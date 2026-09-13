---
description: Ingérer une source depuis raw/ dans le wiki
argument-hint: <nom-du-fichier dans raw/>
---

Ingère la source : $ARGUMENTS

Suis exactement le workflow « Ingérer une source » de CLAUDE.md : lecture, discussion si nécessaire, page(s) wiki avec frontmatter, mise à jour des pages liées, index.md, questions-ouvertes.md, log.md, commit git.

Si $ARGUMENTS est vide : liste les fichiers de raw/ absents de l'index et propose lequel traiter.
