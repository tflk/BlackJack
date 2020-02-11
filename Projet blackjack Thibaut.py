# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:06:42 2020

@author: utilisateur
"""

import numpy as np
import random as rd

def joueurs():
    nbr_joueurs = input("Entrez le nombre de joueurs : ")
    while nbr_joueurs.isnumeric() == False :
        print("Commande invalide.")
        nbr_joueurs = input("Entrez le nombre de joueurs : ")
    prenoms = []
    for k in range(int(nbr_joueurs)):
        prenoms.append(input(("Entrez le nom du joueur "+ str(k+1) + " : ")))
    return prenoms, int(nbr_joueurs)

def pioche_carte(jeu):
    couleur = rd.randint(0, 3)
    while jeu[couleur] == [] :
        couleur = rd.randint(0, 3)
    carte = rd.randint(0, len(jeu[couleur])-1)
    del jeu[couleur][carte]
    return jeu, [carte, couleur]

def init(nbr_joueurs):
    jeu = [[i for i in range(0, 13)] for k in range(4)]
    mains = []
    for k in range(nbr_joueurs + 1) : #+1 pour le croupier
        main = []
        for i in range(2) :
            temp = pioche_carte(jeu)
            jeu = temp[0]
            carte = temp[1]
            main.append(carte)
        mains.append(main)
    return jeu, mains

A = {0 : '♠', 1 : '♥', 2 : '♦', 3 : '♣'}
B = {0 : 1, 1 : 2, 2 : 3, 3 : 4, 4 : 5, 5 : 6, 6 : 7, 7 : 8, 8 : 9, 9 : '1 0',
     10 : 'Valet', 11 : 'Dame ', 12 : 'Roi'}

def afficher_carte(numero, couleur):
    Carte =[['╔═══════╗', '', '', '', ''],
     ['║ ', A[couleur], '   ', A[couleur], ' ║'],
     ['║', '       ', '║', '', ''],
     ['║', str(B[numero]).center(7), '║', '', ''],
     ['║', '       ', '║', '', ''],
     ['║ ', A[couleur], '   ', A[couleur], ' ║'],
     ['╚═══════╝', '', '', '', '']]
    return Carte

def afficher_main(main):
    matmain = afficher_carte(main[0][0], main[0][1])
    main2 = main[1:]
    for carte in main2 :
        temp = afficher_carte(carte[0], carte[1])
        matmain = np.concatenate((matmain, temp), axis = 1)
    for ligne in matmain :
        for carte in ligne :
            print(carte, end = '')
        print()

def points(main):
    points = 0
    as_ = 0
    for carte in main :
        if 0 < carte[0] <= 9 :
            points += carte[0] + 1
        elif carte[0] > 9 :
            points += 10
        elif carte[0] == 0 :
            as_ += 1
            points += 11
    for k in range(as_) :
        if points > 21 :
            points -= 10
    return points

def tour_joueur(jeu, prenom, main_joueur, main_croupier, end_joueur) :
    if end_joueur == False :
        print("Tour de", prenom, ":")
        print("Jeu du croupier :")
        afficher_main(main_croupier)
        print("Points du croupier :", points(main_croupier))
        print("Votre jeu :")
        afficher_main(main_joueur)
        print("Vos points :", points(main_joueur))
        decision = input("Voulez vous tirer une autre carte ? (Y/N) ")
        while decision.lower() != 'y' and decision.lower() != 'n' :
            print("Commande invalide.")
            decision = input("Voulez vous tirer une autre carte ? (Y/N) ")
        if decision.lower() == 'y' :
            temp = pioche_carte(jeu)
            jeu = temp[0]
            print("Vous piochez :")
            afficher_main([temp[1]])
            main_joueur.append(temp[1])
        else :
            end_joueur = True
        if points(main_joueur) > 21 :
            print(prenom, "a dépassé 21, il saute !")
            end_joueur = True
    return jeu, main_joueur, end_joueur

def tour_croupier(jeu, main_croupier, end_croupier):
    print("Tour du croupier :")
    print("Main du croupier :")
    afficher_main(main_croupier)
    points_croupier = points(main_croupier)
    print("Points du croupier :", points_croupier)
    if 17 <= points_croupier <= 21 :
        print("Le croupier s'arrête ici.")
        end_croupier = True
    if points_croupier <= 16 :
        temp = pioche_carte(jeu)
        jeu = temp[0]
        print("Le croupier pioche :")
        afficher_main([temp[1]])
        main_croupier.append(temp[1])
    points_croupier = points(main_croupier)
    if points_croupier > 21 :
        print("Le croupier a dépassé 21, il saute !")
        end_croupier = True
    return jeu, main_croupier, end_croupier

def fin(mains, nbr_joueurs, prenoms):
    point = []
    if mains[nbr_joueurs] == "BlackJack":
        points_croupier = "BlackJack"
    else :
        points_croupier = points(mains[nbr_joueurs])
    for k in range(nbr_joueurs):
        if mains[k] == "BlackJack" :
            point.append("BlackJack")
        else :
            point.append(points(mains[k]))
    for k in range(nbr_joueurs):
        if points_croupier == "BlackJack" :
            if point[k] == "BlackJack" :
                print("Bravo", prenoms[k], "! Vous avez gagné !")
            else :
                print("Désolé", prenoms[k], ", vous avez perdu !")
        else :
            if point[k] == "BlackJack" :
                print("Bravo", prenoms[k], "! Vous avez gagné !")
            else :
                if points_croupier > 21:
                    if points_croupier == point[k]:
                        print("Il y a égalité entre", prenoms[k], "et le croupier !")
                    elif point[k] > points_croupier:
                        print("Bravo", prenoms[k], "! Vous avez gagné !")
                    elif 21 < point[k] < points_croupier:
                        print("Désolé", prenoms[k], ", vous avez perdu !")
                    else :
                        print("Bravo", prenoms[k], "! Vous avez gagné !")     
                else :
                    if points_croupier == point[k]:
                        print("Il y a égalité entre", prenoms[k], "et le croupier !")
                    elif points_croupier > point[k]:
                        print("Désolé", prenoms[k], ", vous avez perdu !")
                    elif points_croupier < point[k] <= 21:
                        print("Bravo", prenoms[k], "! Vous avez gagné !")
                    else :
                        print("Désolé", prenoms[k], ", vous avez perdu !")

def blackjack():
    jou = joueurs()
    prenoms = jou[0]
    nbr_joueurs = jou[1]
    init_ = init(nbr_joueurs)
    jeu = init_[0]
    mains = init_[1]
    end_joueurs = [False for k in range(nbr_joueurs + 1)]
    for k in range(nbr_joueurs) :
        if points(mains[k]) == 21 :
            print(prenoms[k], "a fait un BlackJack !!")
            mains[k] = "BlackJack"
            end_joueurs[k] = True
    if points(mains[nbr_joueurs]) == 21 :
        print("Le croupier a fait un BlackJack ! La partie s'arrête !")
        mains[nbr_joueurs] = "BlackJack"
        end_joueurs = [True for k in range(nbr_joueurs + 1)]
    while end_joueurs != [True for k in range(nbr_joueurs + 1)] :
        for k in range(nbr_joueurs):
            while end_joueurs[k] == False :
                tour_j = tour_joueur(jeu, prenoms[k], mains[k], mains[nbr_joueurs], end_joueurs[k])
                jeu = tour_j[0]
                mains[k] = tour_j[1]
                end_joueurs[k] = tour_j[2]
        if end_joueurs[nbr_joueurs] == False :
            tour_c = tour_croupier(jeu, mains[nbr_joueurs], end_joueurs[nbr_joueurs])
            jeu = tour_c[0]
            mains[nbr_joueurs] = tour_c[1]
            end_joueurs[nbr_joueurs] = tour_c[2]
    fin(mains, nbr_joueurs, prenoms)

