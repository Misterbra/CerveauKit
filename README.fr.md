# CerveauKit — B2Labs
Version 1.1.0 · Kit gratuit · Parcours Windows 10/11

Ouvrez **COMMENCER.html** après avoir extrait tout le ZIP.

## À quoi sert-il ?
Une bibliothèque de travail que vous conservez : vos notes d’origine dans raw/, des fiches sourcées dans wiki/, un index et les questions qui restent ouvertes. Vous demandez à **Claude Code ou Codex** de classer une source, retrouver un fait ou préparer un brief à partir de vos connaissances.
La valeur vient de cette organisation réutilisable, des références aux originaux et des règles de classement communes. Ce n’est ni un modèle IA supplémentaire, ni une application autonome. Pour une seule question sur un seul document, une conversation classique peut suffire.

## Premier résultat
1. Extrayez le ZIP et ouvrez COMMENCER.html. Lisez l’exemple fictif Atelier Exemple, rédigé à l’avance.
2. Double-cliquez VERIFIER.cmd : diagnostic sans installation ni envoi de vos documents.
3. Si nécessaire, INSTALLER.cmd vous propose **1. Claude Code** ou **2. Codex**. Un seul suffit. Chaque installation demande votre accord.
4. OUVRIR-CERVEAU.cmd vous laisse choisir votre assistant. Connectez votre compte : Claude pour Claude Code, ChatGPT avec accès Codex pour Codex. Autorisez uniquement le dossier de votre copie du kit.
5. Demandez : « Lis raw/exemple-atelier.md. Quel est le délai prévu et qu’est-ce qui reste à confirmer ? Cite le passage source. »
6. Ajoutez votre note .txt ou .md dans raw/ puis demandez « Classe raw/ma-note.md dans mon cerveau ». Relisez le résultat.

## Dépendances : un seul assistant suffit
- **Claude Code OU Codex**, Internet et votre propre accès compatible. Le kit ne comprend aucun abonnement ni crédit IA. Une simple session dans le site web Claude ou ChatGPT ne connecte pas automatiquement le dossier : utilisez l’assistant local proposé.
- Claude Code : installation native via WinGet, sans Node.js obligatoire. Un compte Claude gratuit seul ne suffit pas pour Claude Code.
- Codex : si déjà installé, aucune réinstallation. Sinon le lanceur propose Node.js LTS (22 minimum pour ce parcours), puis le paquet officiel @openai/codex via npm. L’accès dépend de votre offre ChatGPT ; une clé API peut aussi entraîner une facturation à l’usage. Ne saisissez aucune clé dans les fichiers du kit.
- **Obsidian et Git : facultatifs.** Tout éditeur de texte lit les fiches. Aucun dépôt distant ni synchronisation n’est créé.
- **Python : uniquement pour la vidéo.** Python 3.12, FFmpeg, Deno et les modules Python sont vérifiés par l’installateur séparé.
- Aucun logiciel tiers n’est embarqué. Les .cmd sont des lanceurs lisibles, pas un .exe autonome.

## Quand se déclenche-t-il ?
À votre demande, jamais tout seul. Copier une note dans raw/ ne déclenche rien.
- « Classe raw/ma-note.md » : prépare une fiche et actualise l’index.
- « Quel délai avons-nous prévu ? Cite tes sources » : recherche une réponse.
- « Fais le bilan de mon cerveau » : synthèse des fiches et questions ouvertes.
- « Vérifie les fiches et leurs sources » : contrôle les références et propose les corrections.
Ces phrases fonctionnent avec les deux assistants. Claude Code dispose aussi de raccourcis /ingest, /digest, /lint et /youtube. Ce ne sont pas des commandes Codex.
Vous pouvez changer d’assistant entre deux sessions : les fichiers restent les mêmes. Les historiques de conversation ne sont pas transférés. Fermez la première session avant de faire modifier les mêmes fiches par l’autre.

## Option vidéo : transcription, puis résumé à la demande
INSTALLER-VIDEOS.cmd propose Python 3.12, FFmpeg et Deno s’ils manquent, crée .venv et installe les modules dedans. Il ne demande aucun compte IA. Le premier traitement télécharge le modèle Whisper ; le profil CPU ne nécessite pas de carte graphique.
Ajoutez un lien autorisé dans youtube.md et lancez TRAITER-VIDEOS.cmd. Il télécharge l’audio, le transcrit localement et enregistre la note dans raw/youtube/. Il traite le lot puis s’arrête : le nom technique « watch » ne signifie pas surveillance permanente.
Ouvrez ensuite Claude Code ou Codex : « Résume et classe raw/youtube/IDENTIFIANT.md en citant les repères horodatés ». La transcription n’est envoyée à l’assistant qu’à cette étape. Pas de seconde connexion IA ni d’appel API caché dans le script Python.
Limites : pas de direct, deux heures maximum par vidéo, audio plafonné à 256 Mo. Les restrictions de YouTube peuvent empêcher le téléchargement ; aucun contournement ni import de cookies du navigateur. Utilisez uniquement des contenus que vous êtes autorisé à télécharger et traiter.
Les échecs sont signalés et les autres vidéos continuent. Relancez le lot pour retenter ; les notes déjà transcrites sont conservées.

## Formats et limites
Commencez par du texte ou du Markdown. Les PDF, scans, DOCX et XLSX peuvent demander une extraction adaptée, non incluse. Ne supposez pas que tous les formats sont lisibles par votre assistant.
Les réponses peuvent être erronées : vérifiez les citations dans raw/. Après modification ou retrait d’une source, demandez la mise à jour des fiches. Aucune promesse de gain chiffré.
Ce kit est individuel : pas de contrôle d’accès d’équipe, connecteur email/CRM, envoi de messages, tâche planifiée ou sauvegarde distante.

## Vos données
Les fichiers sont locaux ; le contenu lu par l’assistant peut être transmis à **Anthropic avec Claude Code, ou OpenAI avec Codex**. Ce n’est pas une IA hors ligne. Whisper transcrit localement après téléchargement du modèle. YouTube reçoit les requêtes de téléchargement. Les installations contactent leurs fournisseurs.
B2Labs ne reçoit pas vos documents via ce kit et n’ajoute pas de télémétrie. Les logiciels tiers gardent leurs propres conditions, réglages et pratiques. Les fichiers CLAUDE.md et AGENTS.md donnent les mêmes consignes ; ils ne remplacent pas les permissions de votre assistant. Vérifiez ces permissions et n’ajoutez pas de connecteurs inutiles.
Ne mettez pas de mots de passe, clés ou informations confidentielles non autorisées dans raw/. Ne repartagez pas une copie déjà utilisée : repartez du ZIP original. Sauvegardez régulièrement votre dossier.

## Dépannage et parcours manuel
- Extrayez tout le ZIP avant de lancer les fichiers.
- Après une installation, fermez les fenêtres et relancez VERIFIER.cmd pour actualiser la détection des outils.
- Si WinGet est absent, installez votre assistant depuis sa documentation officielle ci-dessous. Aucun changement permanent de politique PowerShell n’est appliqué.
- Dans un terminal ouvert à la racine du kit, lancez **claude** ou **codex**. C’est aussi le parcours manuel macOS/Linux ; les lanceurs fournis et les tests ciblent Windows.
- Si un traitement vidéo a été interrompu brutalement, vérifiez qu’il ne tourne plus avant de retirer raw/youtube/.run.lock. Ne supprimez pas ce verrou pendant un traitement actif.
- Pour réparer les modules vidéo, sauvegardez puis relancez INSTALLER-VIDEOS.cmd. Pour changer leurs versions, utilisez une nouvelle version du kit ou faites revalider le fichier de contraintes. Les versions installées sont enregistrées dans .venv/installed-requirements.txt.
- Supprimer votre copie après sauvegarde désinstalle le kit, pas les logiciels tiers.

Documentation officielle :
- Claude Code : https://code.claude.com/docs/en/setup
- Codex : https://developers.openai.com/codex/cli
- Connexion Codex : https://developers.openai.com/codex/auth
- Licences et modules : DEPENDANCES.md
