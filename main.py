import pyautogui
import os
from datetime import datetime
import time

def getnummatches():
        total_matches_ended=0
        total_matches_started=0
        with open(f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Forge\\forge.log', 'r') as f:
            for i in f.read().split('\n'):
                if 'Winner' in i:
                    total_matches_ended+=1
                elif 'forge.gamemodes.match.GameLobby.startGame' in i:
                    total_matches_started+=1
        total_matches_started=int(total_matches_started/2)
        return total_matches_started, total_matches_ended

def salvarlog(mensagem):
    time_format = "%d-%m-%Y %H:%M:%S"
    time=datetime.now()

    time=datetime.strftime(time, time_format)

    with open('resultados.log','a') as f:
        log=f'''
[{time}]
{mensagem}
#################
'''
        f.write(log)

def calculatewins():
    results=[]
    name=[]

    with open(f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Forge\\forge.log', 'r') as f:
        for i in f.read().split('\n'):
            if 'Winner' in i:
                i=i.split(' | ')[1].split(' ')
                results.append(i[-1])
            elif 'was chosen for the lobby player' in i:
                name.append(i.split()[-1][0:-1])

    name=name[-2:]

    name0=0
    name1=0
    for i in results:
        if i == name[0]:
            name0+=1
        else:
            name1+=1

    if name0>name1:
        wins=name0
        winner=name[0]
        winsloser=name1
        loser=name[1]
    else:
        wins=name1
        winner=name[1]
        winsloser=name0
        loser=name[0]

    percent=(wins*100)/(wins+winsloser)
    percentloser=(winsloser*100)/(wins+winsloser)

    mensagem=f'\n{percent:.2f}% de vitória para {winner} ({wins} vitória(s)).\n'
    mensagem+=f'{percentloser:.2f}% de vitória para {loser} ({winsloser} vitória(s)).\n'
    print(mensagem)
    return mensagem

def playmatches():
    num_matches=int(input('Digite o número de partidas para testar: '))

    print('''
Passo a passo:

1. Reinicie o Forge para limpar o histórico de partidas.
2. Configure a partida com dois jogadores IA.
3. Selecione Jogos em partida: 1. Também é recomendável selecionar Personalidade de IA: Random (Every Game) nas preferências de jogabilidade.
4. Clique em START. Assim que a partida começar, clique em 10x speed e NÃO mova o mouse nem aperte mais nenhuma tecla até que o jogo volte ao menu.
5. Quando o jogo voltar ao menu, volte a esta janela para ver os resultados. Eles também estarão disponíveis no arquivo resultados.log
''')

    matches_started_total, matches_ended_total = getnummatches()

    while True:
        matches_started, matches_ended = getnummatches()

        if matches_ended>=num_matches:
            print(f'Partidas jogadas: {matches_ended_total+1}')
            break

        if matches_ended>matches_ended_total:
            matches_ended_total=matches_ended
            print(f'Partidas jogadas: {matches_ended_total}')
            time.sleep(4)
            pyautogui.press('space')
            time.sleep(4)
            pyautogui.press('esc')

def main():
    with open(f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Forge\\forge.log', 'a') as f:
        ...
    playmatches()
    salvarlog(calculatewins())
    input('Pressione ENTER para testar outra partida (reinicie o Forge antes!)')
    print('\n'+'#'*30+'\n')
    main()


try:
    os.makedirs(f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Forge')
except:
    ...

main()