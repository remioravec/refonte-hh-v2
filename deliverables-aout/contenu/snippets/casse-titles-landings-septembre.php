<?php
/**
 * A AJOUTER dans l'extrait 12, « Casse francaise des titles refondus (Claude) ».
 *
 * POURQUOI — le site capitalise chaque mot du title RENDU. Constat du
 * 27/08/2026, toujours vrai le 17/09/2026. L'extrait 12 corrige deja cinq
 * contenus par une liste blanche ; les trois landings de septembre n'y sont
 * pas, donc leurs titles ressortent avec « Et », « Au », « De », « Des »,
 * « Sans » capitalises — ce qui n'est pas de la typographie francaise.
 *
 * Les titles STOCKES en base sont corrects : c'est le rendu qu'il faut
 * corriger, et l'extrait 12 est deja le bon endroit pour le faire.
 *
 * COMMENT — ouvrir l'extrait 12 et ajouter ces trois lignes dans le tableau
 * retourne par hh_titles_refondus(), avant l'accolade fermante. Rien d'autre
 * a changer : le reste de l'extrait fait deja le travail.
 */

		11955 => 'ERP Fruits et Légumes : Agréage, Poids Réel et Marge au Lot',
		11957 => 'ERP Produits de la Mer : Criée, Marée et Traçabilité des Lots',
		11959 => "ERP PME Agroalimentaire : Sortir d'Excel sans Tout Casser",
