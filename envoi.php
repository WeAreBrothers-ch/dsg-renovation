<?php
/* ============================================================
   DSG RÉNOVATION — RÉCEPTION DU BORDEREAU DE DEMANDE
   Reçoit la demande de devis, la vérifie, puis l'envoie par
   courriel à l'entreprise, photos du chantier jointes.

   Deux façons d'arriver ici :
   - avec JavaScript, formulaire.js poste la demande et attend
     du JSON : le statut HTTP dit si elle est partie, et un refus
     porte un message par champ ;
   - sans JavaScript, le formulaire est soumis normalement : le
     visiteur est renvoyé vers merci.html, ou vers le formulaire
     si la demande n'a pas pu partir.

   Rien n'est conservé : les photos ne quittent pas le dossier
   temporaire de PHP, qui les efface en fin de requête. Seule la
   limitation du débit garde quelques minutes des horodatages,
   rangés sous une empreinte de l'adresse IP, jamais l'adresse.

   PHP 8.0 ou plus récent, extension fileinfo, fonction mail().
   ============================================================ */

declare(strict_types=1);

/* ---------- Réglages ---------- */

/* Adresse qui reçoit les demandes. */
const DESTINATAIRE = 'contact@dsg-renov.ch';

/* Expéditeur des courriels. Infomaniak refuse un expéditeur hors du
   domaine : l'adresse doit exister sur dsg-renov.ch. Elle reçoit aussi
   les avis de non-distribution ; la réponse, elle, part vers le
   visiteur (Reply-To) quand il a laissé son courriel. */
const EXPEDITEUR = 'Site DSG Rénovation <contact@dsg-renov.ch>';

/* Pages où renvoyer le visiteur qui envoie sans JavaScript. */
const PAGE_MERCI = 'merci.html';
const PAGE_ERREUR = 'devis.html?erreur=1#formulaire';

/* Fuseau de l'heure de réception inscrite dans le courriel. */
const FUSEAU = 'Europe/Zurich';

/* Champs du bordereau, dans l'ordre du courriel : libellé, puis
   longueur maximale en caractères. */
const CHAMPS = [
    'travaux'   => ['Travaux concernés', 500],
    'type'      => ['Type de bien', 200],
    'lieu'      => ['Commune du bien', 200],
    'surface'   => ['Surface approximative', 200],
    'delai'     => ['Démarrage souhaité', 200],
    'message'   => ['Description du projet', 5000],
    'nom'       => ['Nom', 200],
    'telephone' => ['Téléphone', 200],
    'email'     => ['Courriel', 254],
    'rappel'    => ['Rappel souhaité', 200],
];

/* Photos du chantier : nombre de fichiers, poids d'un fichier, poids
   total. Le PHP du serveur doit suivre : upload_max_filesize au moins
   égal au poids d'un fichier, post_max_size un peu au-dessus du total. */
const PHOTOS_MAX = 6;
const PHOTO_OCTETS_MAX = 8 * 1024 * 1024;
const PHOTOS_OCTETS_MAX = 20 * 1024 * 1024;

/* Types acceptés, reconnus au contenu du fichier et non à son nom,
   avec l'extension que prend la pièce jointe. */
const TYPES_PHOTOS = [
    'image/jpeg' => 'jpg',
    'image/png'  => 'png',
    'image/webp' => 'webp',
    'image/heic' => 'heic',
    'image/heif' => 'heif',
];

/* Limitation du débit : ENVOIS_MAX demandes au plus par adresse IP
   sur une fenêtre glissante de FENETRE_SECONDES. */
const ENVOIS_MAX = 5;
const FENETRE_SECONDES = 600;

/* ---------- Réponses ---------- */

/** Le navigateur attend-il du JSON, comme formulaire.js ? */
function attend_json(): bool
{
    return stripos((string) ($_SERVER['HTTP_ACCEPT'] ?? ''), 'application/json') !== false;
}

/**
 * Répond, puis termine le script. Avec JavaScript : le statut HTTP et
 * un corps JSON. Sans : une redirection vers la page de remerciement,
 * ou vers le formulaire si la demande n'est pas partie.
 *
 * @param int $statut code HTTP
 * @param array<string, string> $erreurs message par champ
 */
function repondre(int $statut, array $erreurs = []): void
{
    if (attend_json()) {
        $corps = ['ok' => $statut < 300];
        if ($erreurs !== []) {
            $corps['erreurs'] = $erreurs;
        }
        http_response_code($statut);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($corps, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE);
    } elseif ($statut === 405) {
        /* Une simple visite de l'adresse : rien à montrer. */
        http_response_code(405);
        header('Content-Type: text/plain; charset=utf-8');
        echo "Méthode non autorisée.\n";
    } else {
        header('Location: ' . ($statut < 300 ? PAGE_MERCI : PAGE_ERREUR), true, 303);
    }
    exit;
}

/* ---------- Champs ---------- */

/**
 * Nettoie un texte saisi : caractères de contrôle retirés, espaces
 * superflus supprimés. Seule la description garde ses retours à la
 * ligne ; ailleurs, rien ne doit pouvoir couper une ligne d'en-tête.
 */
function nettoyer(string $texte, bool $multiligne): string
{
    $texte = (string) preg_replace('/\r\n?|[\x{2028}\x{2029}]/u', "\n", $texte);
    if ($multiligne) {
        $texte = (string) preg_replace('/[^\P{Cc}\n\t]/u', '', $texte);
        $texte = (string) preg_replace('/\h+$/mu', '', $texte);
        $texte = (string) preg_replace('/\n{3,}/', "\n\n", $texte);
    } else {
        $texte = (string) preg_replace('/[\s\p{Cc}]+/u', ' ', $texte);
    }
    return (string) preg_replace('/^\s+|\s+$/u', '', $texte);
}

/**
 * Valeur d'un champ texte, nettoyée. « travaux » arrive joint par
 * formulaire.js, ou en plusieurs valeurs travaux[] sans JavaScript.
 *
 * @return string|null null si la valeur est illisible : UTF-8 invalide,
 *                     ou tableau là où l'on attend un texte
 */
function lire_champ(string $nom): ?string
{
    $brut = $_POST[$nom] ?? '';
    $valeurs = [];
    foreach ((is_array($brut) && $nom === 'travaux') ? $brut : [$brut] as $valeur) {
        if (!is_string($valeur) || preg_match('//u', $valeur) !== 1) {
            return null;
        }
        $valeur = nettoyer($valeur, $nom === 'message');
        if ($valeur !== '') {
            $valeurs[] = $valeur;
        }
    }
    return implode(', ', $valeurs);
}

/** Nombre de caractères (et non d'octets) d'un texte UTF-8. */
function longueur(string $texte): int
{
    return (int) preg_match_all('/./su', $texte);
}

/**
 * Adresse de courriel acceptable : le motif de formulaire.js, sans
 * guillemets, puis le contrôle de PHP. Rien qui puisse sortir de
 * l'en-tête Reply-To.
 */
function courriel_valide(string $courriel): bool
{
    return preg_match('/^[^\s@"]+@[^\s@]+\.[a-z]{2,}$/i', $courriel) === 1
        && filter_var($courriel, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Lit et vérifie les champs texte, avec les règles de formulaire.js.
 *
 * @param array<string, string> $erreurs reçoit un message par champ fautif
 * @return array<string, string> valeurs nettoyées, par nom de champ
 */
function verifier_champs(array &$erreurs): array
{
    $donnees = [];
    foreach (CHAMPS as $nom => [$libelle, $maximum]) {
        $valeur = lire_champ($nom);
        if ($valeur === null) {
            $erreurs[$nom] = "Le champ « {$libelle} » contient des caractères illisibles.";
        } elseif (longueur($valeur) > $maximum) {
            $erreurs[$nom] = "Le champ « {$libelle} » est trop long : {$maximum} caractères au maximum.";
        }
        $donnees[$nom] = $valeur ?? '';
    }

    $obligatoires = [
        'nom' => 'Indiquez votre nom pour que nous sachions qui rappeler.',
        'telephone' => 'Indiquez un numéro de téléphone pour que nous puissions vous rappeler.',
        'message' => 'Décrivez votre projet en quelques mots : pièces concernées, travaux envisagés.',
    ];
    foreach ($obligatoires as $nom => $message) {
        if (!isset($erreurs[$nom]) && $donnees[$nom] === '') {
            $erreurs[$nom] = $message;
        }
    }

    $chiffres = (string) preg_replace('/[^0-9]/', '', $donnees['telephone']);
    if (!isset($erreurs['telephone']) && strlen($chiffres) < 9) {
        $erreurs['telephone'] = 'Le numéro de téléphone paraît incomplet : il faut au moins 9 chiffres.';
    }
    if (!isset($erreurs['email']) && $donnees['email'] !== '' && !courriel_valide($donnees['email'])) {
        $erreurs['email'] = "L'adresse de courriel paraît invalide : vérifiez-la, ou laissez le champ vide.";
    }
    return $donnees;
}

/* ---------- Photos ---------- */

/**
 * Photos reçues dans photos[], mises à plat. Un champ de fichier
 * laissé vide arrive quand même, sans fichier : on l'écarte.
 *
 * @return list<array{nom: string, chemin: string, erreur: int, taille: int}>
 */
function photos_recues(): array
{
    $brut = $_FILES['photos'] ?? null;
    if (!is_array($brut) || !isset($brut['name'], $brut['tmp_name'], $brut['error'], $brut['size'])) {
        return [];
    }
    /* photos[] donne une liste par propriété ; un champ « photos » sans
       crochets, des valeurs seules : on se ramène au premier cas. */
    if (!is_array($brut['name'])) {
        $brut = array_map(static fn($valeur): array => [$valeur], $brut);
    }
    $photos = [];
    foreach ($brut['name'] as $i => $nom) {
        $erreur = $brut['error'][$i] ?? UPLOAD_ERR_NO_FILE;
        if (!is_string($nom) || !is_int($erreur) || $erreur === UPLOAD_ERR_NO_FILE) {
            continue;
        }
        $photos[] = [
            'nom' => $nom,
            'chemin' => (string) ($brut['tmp_name'][$i] ?? ''),
            'erreur' => $erreur,
            'taille' => (int) ($brut['size'][$i] ?? 0),
        ];
    }
    return $photos;
}

/**
 * Nom de fichier sans risque pour un en-tête de courriel : sans chemin
 * ni accents, réduit aux lettres, chiffres, points, tirets et soulignés.
 */
function assainir_nom(string $nom): string
{
    $nom = (string) preg_replace('~^.*[/\\\\]~s', '', $nom);
    /* « é » devient « &eacute; », dont on garde la lettre de base. */
    $nom = htmlentities($nom, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    $nom = (string) preg_replace('/&([A-Za-z]{1,2})(?:acute|grave|circ|tilde|uml|ring|cedil|slash|caron|lig);/', '$1', $nom);
    $nom = (string) preg_replace('/&[^;]*;|[^A-Za-z0-9._&-]+/', '-', $nom);
    /* Ni tiret collé à un point, ni points répétés, ni tiret en tête. */
    $nom = (string) preg_replace(['/[-.]*\.[-.]*/', '/-{2,}/'], ['.', '-'], $nom);
    $nom = rtrim(ltrim($nom, '-'), '-.');
    return substr($nom === '' || $nom[0] === '.' ? 'photo' . $nom : $nom, 0, 100);
}

/**
 * Vérifie les photos : nombre, poids, et type reconnu au contenu du
 * fichier. Elles restent où PHP les a déposées ; seul leur contenu
 * part, en pièce jointe.
 *
 * @param list<array{nom: string, chemin: string, erreur: int, taille: int}> $photos
 * @param array<string, string> $erreurs reçoit le message du champ photos
 * @param bool $trop_lourd passe à vrai quand le refus tient au poids
 * @return list<array{nom: string, type: string, chemin: string}> pièces jointes
 */
function verifier_photos(array $photos, array &$erreurs, bool &$trop_lourd): array
{
    if ($photos === []) {
        return [];
    }
    if (count($photos) > PHOTOS_MAX) {
        $erreurs['photos'] = sprintf('Joignez %d photos au plus.', PHOTOS_MAX);
        return [];
    }
    $plafond = min(PHOTO_OCTETS_MAX, octets_ini('upload_max_filesize'));
    $detecteur = new finfo(FILEINFO_MIME_TYPE);
    $pieces = [];
    $pris = [];
    $total = 0;

    foreach ($photos as $photo) {
        $nom = assainir_nom($photo['nom']);
        if (in_array($photo['erreur'], [UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE], true) || $photo['taille'] > $plafond) {
            $trop_lourd = true;
            $erreurs['photos'] = sprintf('La photo « %s » dépasse %s Mo.', $nom, mo($plafond));
            return [];
        }
        if ($photo['erreur'] === UPLOAD_ERR_PARTIAL) {
            $erreurs['photos'] = sprintf("La photo « %s » n'est pas arrivée entière. Réessayez.", $nom);
            return [];
        }
        /* Dossier temporaire absent, disque plein… : le serveur est en cause. */
        if ($photo['erreur'] !== UPLOAD_ERR_OK || !is_uploaded_file($photo['chemin'])) {
            throw new RuntimeException('photo non reçue, code ' . $photo['erreur']);
        }
        $type = $detecteur->file($photo['chemin']);
        if (!is_string($type) || !array_key_exists($type, TYPES_PHOTOS)) {
            $erreurs['photos'] = sprintf("Le fichier « %s » n'est pas une photo JPEG, PNG, WebP ou HEIC.", $nom);
            return [];
        }
        $total += $photo['taille'];

        /* L'extension suit le contenu ; deux photos homonymes restent distinctes. */
        $base = trim(substr((string) preg_replace('/\.[^.]*$/', '', $nom), 0, 60), '-._');
        $base = $base !== '' ? $base : 'photo';
        $piece = $base . '.' . TYPES_PHOTOS[$type];
        for ($n = 2; in_array(strtolower($piece), $pris, true); $n++) {
            $piece = $base . '-' . $n . '.' . TYPES_PHOTOS[$type];
        }
        $pris[] = strtolower($piece);
        $pieces[] = ['nom' => $piece, 'type' => $type, 'chemin' => $photo['chemin']];
    }

    if ($total > PHOTOS_OCTETS_MAX) {
        $trop_lourd = true;
        $erreurs['photos'] = sprintf('Les photos dépassent %s Mo au total.', mo(PHOTOS_OCTETS_MAX));
        return [];
    }
    return $pieces;
}

/* ---------- Limitation du débit ---------- */

/**
 * Dossier des compteurs, dans le dossier temporaire du système. Celui-ci
 * peut être partagé entre comptes : on ne se sert du nôtre que s'il est
 * un vrai dossier, fermé aux autres.
 */
function dossier_compteurs(): ?string
{
    $dossier = rtrim(sys_get_temp_dir(), '/\\') . '/dsg-renovation-devis';
    if (!is_dir($dossier)) {
        @mkdir($dossier, 0700);
    }
    $droits = @fileperms($dossier);
    if (is_link($dossier) || !is_dir($dossier) || $droits === false || ($droits & 0077) !== 0) {
        return null;
    }
    return $dossier;
}

/**
 * Sel secret des empreintes, tiré au hasard la première fois puis relu.
 * Il ne quitte pas le serveur : sans lui, impossible de retrouver une
 * adresse IP en essayant toutes les adresses possibles.
 */
function sel(string $dossier): ?string
{
    $fichier = $dossier . '/sel';
    $sel = @file_get_contents($fichier);
    if (is_string($sel) && strlen($sel) === 32) {
        return $sel;
    }
    /* Écrit à côté puis renommé : un envoi simultané ne lit jamais un
       sel à moitié écrit. */
    $sel = random_bytes(32);
    $provisoire = $fichier . '-' . bin2hex(random_bytes(8));
    if (@file_put_contents($provisoire, $sel) === 32 && @rename($provisoire, $fichier)) {
        return $sel;
    }
    @unlink($provisoire);
    return null;
}

/**
 * Compte cette demande et dit s'il faut patienter. Chaque adresse IP a
 * son fichier, nommé par une empreinte salée (HMAC-SHA256) : l'adresse
 * n'est jamais écrite, le fichier ne contient que des horodatages. Si
 * les fichiers font défaut, la demande passe : mieux vaut un envoi de
 * trop qu'une demande perdue.
 *
 * @return int secondes à patienter, 0 si la demande peut partir
 */
function limiter_debit(string $ip): int
{
    $dossier = dossier_compteurs();
    $sel = $dossier !== null ? sel($dossier) : null;
    if ($dossier === null || $sel === null) {
        error_log('envoi.php : limitation du débit inactive, dossier temporaire inutilisable.');
        return 0;
    }

    /* En IPv6, un abonné dispose d'un bloc /64 entier : il compte pour une adresse. */
    $binaire = @inet_pton($ip);
    if (is_string($binaire) && strlen($binaire) === 16) {
        $binaire = substr($binaire, 0, 8);
    }
    $empreinte = hash_hmac('sha256', is_string($binaire) ? $binaire : $ip, $sel);
    $poignee = @fopen($dossier . '/' . $empreinte . '.txt', 'c+');
    if ($poignee === false) {
        return 0;
    }

    flock($poignee, LOCK_EX);
    $maintenant = time();
    $recents = [];
    foreach (explode("\n", (string) stream_get_contents($poignee)) as $ligne) {
        if ((int) $ligne > $maintenant - FENETRE_SECONDES) {
            $recents[] = (int) $ligne;
        }
    }
    $attente = count($recents) >= ENVOIS_MAX ? min($recents) + FENETRE_SECONDES - $maintenant : 0;
    if ($attente === 0) {
        $recents[] = $maintenant;
        ftruncate($poignee, 0);
        rewind($poignee);
        fwrite($poignee, implode("\n", $recents) . "\n");
        fflush($poignee);
    }
    flock($poignee, LOCK_UN);
    fclose($poignee);

    /* Les compteurs restés muets une fenêtre entière ne servent plus. */
    foreach (glob($dossier . '/*.txt') ?: [] as $fichier) {
        if (@filemtime($fichier) < $maintenant - FENETRE_SECONDES) {
            @unlink($fichier);
        }
    }
    return $attente;
}

/* ---------- Courriel ---------- */

/**
 * Texte prêt pour un en-tête de courriel (RFC 2047). Au-delà des lettres
 * sans accent, des chiffres et des espaces, il passe en mots encodés
 * base64, découpés sans couper un caractère et repliés au besoin : aucun
 * retour à la ligne venu du visiteur ne peut y survivre.
 */
function encoder_entete(string $texte): string
{
    if (preg_match('/^[A-Za-z0-9 ]*$/', $texte) === 1) {
        return $texte;
    }
    $mots = [];
    $mot = '';
    foreach (preg_split('//u', $texte, -1, PREG_SPLIT_NO_EMPTY) ?: [] as $caractere) {
        if (strlen($mot . $caractere) > 42) {
            $mots[] = $mot;
            $mot = '';
        }
        $mot .= $caractere;
    }
    $mots[] = $mot;
    return implode("\r\n ", array_map(static fn(string $m): string => '=?UTF-8?B?' . base64_encode($m) . '?=', $mots));
}

/** Adresse précédée d'un nom affiché, pour un en-tête From ou Reply-To. */
function adresse(string $nom, string $courriel): string
{
    return $nom === '' ? $courriel : encoder_entete($nom) . ' <' . $courriel . '>';
}

/**
 * Sépare « Nom <adresse> » en nom et adresse.
 *
 * @return array{0: string, 1: string}
 */
function decomposer(string $expediteur): array
{
    if (preg_match('/^(.*)<([^<>]+)>\s*$/su', $expediteur, $morceaux) === 1) {
        return [trim($morceaux[1], " \t\""), trim($morceaux[2])];
    }
    return ['', trim($expediteur)];
}

/**
 * Texte du courriel : les réponses dans l'ordre du bordereau, une
 * valeur absente valant « — ».
 *
 * @param array<string, string> $donnees
 */
function rediger(array $donnees, int $photos, DateTimeImmutable $recu): string
{
    $lignes = [
        'Demande de devis déposée depuis le site dsg-renov.ch',
        'Reçue le ' . $recu->format('d.m.Y') . ' à ' . $recu->format('H:i'),
        '',
    ];
    foreach (CHAMPS as $nom => [$libelle]) {
        $valeur = $donnees[$nom] !== '' ? $donnees[$nom] : '—';
        if (strpos($valeur, "\n") === false) {
            $lignes[] = $libelle . ' : ' . $valeur;
        } else {
            /* Une description sur plusieurs lignes se lit d'un bloc. */
            array_push($lignes, '', $libelle . ' :', $valeur, '');
        }
    }
    $lignes[] = 'Photos jointes : ' . $photos;
    return str_replace("\n", "\r\n", implode("\n", $lignes)) . "\r\n";
}

/**
 * Confie le courriel à la messagerie du serveur. L'option -f fixe
 * l'adresse de retour des avis de non-distribution ; si le serveur la
 * refuse, on réessaie sans elle.
 *
 * @param array<string, string> $entetes
 */
function poster(string $objet, string $corps, array $entetes, string $retour): bool
{
    if (!function_exists('mail')) {
        return false;
    }
    return mail(DESTINATAIRE, $objet, $corps, $entetes, '-f' . $retour)
        || mail(DESTINATAIRE, $objet, $corps, $entetes);
}

/**
 * Compose le courriel de la demande, photos jointes, puis l'envoie.
 *
 * @param array<string, string> $donnees
 * @param list<array{nom: string, type: string, chemin: string}> $pieces
 */
function envoyer(array $donnees, array $pieces): bool
{
    [$nom_expediteur, $adresse_expediteur] = decomposer(EXPEDITEUR);
    if (filter_var($adresse_expediteur, FILTER_VALIDATE_EMAIL) === false) {
        throw new RuntimeException('EXPEDITEUR ne contient pas une adresse valide');
    }
    $recu = new DateTimeImmutable('now', new DateTimeZone(FUSEAU));
    $texte = quoted_printable_encode(rediger($donnees, count($pieces), $recu));

    $entetes = ['From' => adresse($nom_expediteur, $adresse_expediteur)];
    if ($donnees['email'] !== '') {
        $entetes['Reply-To'] = adresse($donnees['nom'], $donnees['email']);
    }
    $entetes['Date'] = $recu->format(DATE_RFC2822);
    $entetes['Message-ID'] = '<' . bin2hex(random_bytes(16)) . strstr($adresse_expediteur, '@') . '>';
    $entetes['MIME-Version'] = '1.0';

    if ($pieces === []) {
        $entetes['Content-Type'] = 'text/plain; charset=UTF-8';
        $entetes['Content-Transfer-Encoding'] = 'quoted-printable';
        $corps = $texte;
    } else {
        /* « =_ » n'apparaît jamais en quoted-printable ni en base64 : la
           frontière ne peut pas se confondre avec le contenu. */
        $frontiere = '=_' . bin2hex(random_bytes(16));
        $entetes['Content-Type'] = 'multipart/mixed; boundary="' . $frontiere . '"';
        $corps = "--{$frontiere}\r\n"
            . "Content-Type: text/plain; charset=UTF-8\r\n"
            . "Content-Transfer-Encoding: quoted-printable\r\n\r\n"
            . $texte . "\r\n";
        foreach ($pieces as $piece) {
            $contenu = file_get_contents($piece['chemin']);
            if ($contenu === false) {
                throw new RuntimeException('photo illisible dans le dossier temporaire');
            }
            $corps .= "--{$frontiere}\r\n"
                . "Content-Type: {$piece['type']}; name=\"{$piece['nom']}\"\r\n"
                . "Content-Transfer-Encoding: base64\r\n"
                . "Content-Disposition: attachment; filename=\"{$piece['nom']}\"\r\n\r\n";
            $corps .= chunk_split(base64_encode($contenu), 76, "\r\n");
        }
        $corps .= "--{$frontiere}--\r\n";
    }

    return poster(encoder_entete('Demande de devis — ' . $donnees['nom']), $corps, $entetes, $adresse_expediteur);
}

/* ---------- Outils ---------- */

/**
 * Taille donnée par une directive de php.ini (« 8M », « 1G »…), en
 * octets. Une directive nulle ou illisible ne limite rien.
 */
function octets_ini(string $directive): int
{
    $valeur = trim((string) ini_get($directive));
    $unites = ['k' => 1024, 'm' => 1048576, 'g' => 1073741824];
    $octets = (int) $valeur * ($unites[strtolower(substr($valeur, -1))] ?? 1);
    return $octets > 0 ? $octets : PHP_INT_MAX;
}

/** Poids en mégaoctets, écrit à la française : « 8 », « 1,5 ». */
function mo(int $octets): string
{
    return str_replace('.', ',', (string) round($octets / 1048576, 1));
}

/* ---------- Déroulé ---------- */

function traiter(): void
{
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        header('Allow: POST');
        repondre(405);
    }

    /* Au-delà de post_max_size, PHP écarte toute la requête : $_POST et
       $_FILES arrivent vides. Presque toujours des photos trop lourdes. */
    $plafond = octets_ini('post_max_size');
    if ($_POST === [] && $_FILES === [] && (int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > $plafond) {
        repondre(413, ['photos' => sprintf('Les photos sont trop lourdes : %s Mo au total au maximum.', mo(min(PHOTOS_OCTETS_MAX, $plafond)))]);
    }

    /* Un robot a rempli le piège : on fait mine d'avoir reçu. */
    if (($_POST['site_web'] ?? '') !== '') {
        repondre(200);
    }

    $erreurs = [];
    $trop_lourd = false;
    $donnees = verifier_champs($erreurs);
    $pieces = verifier_photos(photos_recues(), $erreurs, $trop_lourd);
    if ($erreurs !== []) {
        repondre($trop_lourd ? 413 : 422, $erreurs);
    }

    $attente = limiter_debit((string) ($_SERVER['REMOTE_ADDR'] ?? ''));
    if ($attente > 0) {
        header('Retry-After: ' . $attente);
        repondre(429, ['formulaire' => 'Plusieurs demandes sont déjà parties depuis cette connexion. Réessayez dans quelques minutes.']);
    }

    if (!envoyer($donnees, $pieces)) {
        error_log("envoi.php : mail() a échoué, la demande n'est pas partie.");
        repondre(500);
    }
    repondre(200);
}

/* ---------- Point d'entrée ---------- */

ini_set('display_errors', '0');
header_remove('X-Powered-By');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

try {
    traiter();
} catch (Throwable $erreur) {
    error_log(sprintf('envoi.php : %s (%s:%d)', $erreur->getMessage(), basename($erreur->getFile()), $erreur->getLine()));
    repondre(500);
}
