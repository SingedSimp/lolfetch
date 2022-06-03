import riotwatcher as rw
from dotenv import load_dotenv
from os import environ
import sys


def get_champs(lol_watcher: rw.LolWatcher, region: str):
    versions = lol_watcher.data_dragon.versions_for_region(region)
    champions_version = versions["n"]["champion"]
    clist = lol_watcher.data_dragon.champions(champions_version)["data"]
    cdict = {}
    for champion in clist:
        cdict[str(clist[champion]["key"])] = champion
    return cdict


def id_to_champ(clist: dict, cid):
    return clist[str(cid)]


# Put 0 for total and it will print all champs
def get_top_champs(lol_watcher: rw.LolWatcher, summoner: str, region: str, total: int):
    me = lol_watcher.summoner.by_name(region, summoner)
    myid = me["id"]
    mastery = lol_watcher.champion_mastery.by_summoner(region, myid)
    cdict = get_champs(lol_watcher, region)
    count = 0
    champs = []
    for champ in mastery:
        cc = []
        cc.append(id_to_champ(cdict, champ["championId"]))
        cc.append(champ["championPoints"])
        champs.append(cc)
        count += 1
        if count == total:
            break
    return champs


def main():
    load_dotenv()
    key = environ["API"]
    lol_watcher = rw.LolWatcher(key)
    my_region = sys.argv[2]
    name = sys.argv[1]
    champs = get_top_champs(lol_watcher, name, my_region, 1)
    topchamps = get_top_champs(lol_watcher, name, my_region, 4)
    me = lol_watcher.summoner.by_name(my_region, name)
    myid = me["id"]
    profile = lol_watcher.league.by_summoner(my_region, myid)[0]
    #print(me)
    #print(profile)
    for champ in champs:
        with open(f"/home/eclipse/rito/icons/{champ[0]}") as f:
            read = f.readlines()
            count = 0
            for line in read:
                if count == 0:
                    print(
                        f"{read[count].strip()}  \033[96m{name}\033[00m@\033[96m{my_region.upper()}\033[00m"
                    )
                elif count == 1:
                    print(
                        f"{read[count].strip()}  {'-' * (len(name) + 1 + len(my_region))}"
                    )
                elif count == 2:
                    print(
                        f"{read[count].strip()}  \033[96mSummoner Level\033[00m: {me['summonerLevel']}"
                    )
                elif count == 3:
                    print(
                        f"{read[count].strip()}  \033[96mMost Played\033[00m: {champ[0]}, {champ[1]} points"
                    )
                elif count == 4:
                    print(
                        f"{read[count].strip()}  \033[96mRank\033[00m: {profile['tier'].title()} {profile['rank']}, {profile['leaguePoints']}LP"
                    )
                elif count == 5:
                    print(
                        f"{read[count].strip()}  \033[96mWins\033[00m: {profile['wins']} wins"
                    )
                elif count == 6:
                    print(
                        f"{read[count].strip()}  \033[96mLosses\033[00m: {profile['losses']} losses"
                    )
                elif count == 7:
                    print(
                        f"{read[count].strip()}  \033[96mGames Played\033[00m: {int(profile['wins']) + int(profile['losses'])}"
                    )
                elif count == 8:
                    print(
                        f"{read[count].strip()}  \033[96mWinrate\033[00m: {(int(profile['wins']) / ( int(profile['wins']) + int(profile['losses']) )) // 0.01}\b\b% winrate"
                    )
                elif count == 9:
                    print(f"{read[count].strip()}  \033[96mTop Champions\033[00m: ")
                elif count == 10:
                    print(
                        f"{read[count].strip()}  {topchamps[1][0]}, {topchamps[1][1]} points"
                    )
                elif count == 11:
                    print(
                        f"{read[count].strip()}  {topchamps[2][0]}, {topchamps[2][1]} points"
                    )
                elif count == 12:
                    print(
                        f"{read[count].strip()}  \033[00m{topchamps[3][0]}, {topchamps[3][1]} points"
                    )

                else:
                    print(line.strip())
                count += 1


if __name__ == "__main__":
    main()
