import discord
from discord.ext import commands
from TK import Token
import requests
import re
import json
from discord.ext import tasks
from itertools import cycle

status = cycle(["워프레임", "< 도움으로 사용 가능합니다", "개발자: PINK_POMA#6293"])
bot = commands.Bot(command_prefix='< ')
Url = 'https://api.warframestat.us/pc/ko'
QUrl = 'https://api.warframestat.us/'


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print('로그인...')
    print(f"봇 {bot.user.name}연결중...")
    print('연결이 완료되었습니다!')
    change_status.start()


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.command()
async def 중재(ctx):
    arbitration_response = requests.get(Url + '/arbitration')
    FTime = arbitration_response.json()['expiry']
    start = FTime.find('T') + 1
    end = FTime.find('.', start)
    Time = FTime[start:end]
    KrTime = 0
    KrTime += (60 * int(Time[0:2]))
    KrTime += int(Time[3:5]) + 780
    Kh = KrTime / 60
    if Kh >= 24:
        Kh -= 24
    Kh = int(Kh)
    Km = KrTime % 60
    TKh = str(Kh)
    if Kh < 10:
        TKh.zfill(2)
    TKm = str(Km)
    TTime = str(Time)
    txt= "KrTime: " + TTime + '\nKh: ' + TKh + "\nKm: " + TKm
    print(txt)
    print("status:{}".format(arbitration_response.status_code))
    if arbitration_response.status_code == 200:
        print(arbitration_response.json())
    embed = discord.Embed(title="중재 정보", description='**　**', color= 0x00ff56)
    embed.add_field(name=":crossed_swords:현재 진영:crossed_swords:**   **", value='​    '+ arbitration_response.json()['enemy'], inline=True)
    embed.add_field(name=":zap:미션 타입:zap:", value='​   ' + arbitration_response.json()['type'], inline=True)
    embed.add_field(name="**       ** :ringed_planet:노드:ringed_planet:", value=arbitration_response.json()['node'], inline=True)
    if Kh < 10:
        embed.add_field(name=":clock" + TKh + ":종료 시각:clock" + TKh +":",value=TKh + "시 " + TKm + "분", inline=True)

    if arbitration_response.json()['archwing'] == True:
        embed.add_field(name="아크윙 사용 가능", inline=False)

    if arbitration_response.json()['sharkwing'] == True:
        embed.add_field(name="샤크윙 사용 가능", inline=False)

    await ctx.send(embed=embed)


""" # 개발중
@bot.command() 
async def 얼럿(ctx):
    alerts_response = requests.get(Url + '/alerts')
    embed = discord.Embed(title="얼럿 정보", description='**　**', color=0x00ff56)
    if alerts_response.json() == '':
        print("얼럿 없음")
        embed.add_field(name=":현재 얼럿이 없습니다!", inline=True)
"""


@bot.command()
async def 데이모스(ctx):
    cambion_response = requests.get(Url + '/cambionCycle')
    embed = discord.Embed(title="캠비온 퇴적지 정보", color=0xff0000)
    embed.set_image(url="https://i.imgur.com/AJnwuQv.png")
    print("시작...")
    print(cambion_response.status_code)
    if cambion_response.status_code == 200:
        if cambion_response.json()['active'] == 'vome':
            embed.add_field(name="현재 진영", value="파스",inline=True)
        else:
            embed.add_field(name="현재 진영", value="봄", inline=True)

        embed.add_field(name="남은 시간", value=cambion_response.json()['timeLeft'] + " 남았습니다",inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def 아이돌론평원(ctx):
    cetus_response = requests.get(Url + '/cetusCycle')
    embed = discord.Embed(title="시터스 정보", color=0x7fa0f4)
    finder=cetus_response.json()['shortString']
    embed.set_image(url="https://i.imgur.com/eGbJ4u1.png")
    nextTime = finder.find('to')+3
    nextday = finder.find('t', nextTime)
    print(finder[nextTime:nextday + 1])
    print("시작...")
    print(cetus_response.status_code)
    if cetus_response.status_code == 200:
        if cetus_response.json()['isDay'] == True:
            embed.add_field(name="현재 상태", value="낮",inline=True)
        else:
            embed.add_field(name="현재 상태", value="밤", inline=True)
        if finder[nextTime:nextday + 1] == 'Night':
            embed.add_field(name="남은 시간", value=cetus_response.json()['timeLeft'] + " 이후 낮으로 바뀝니다",inline=False)
        else:
            embed.add_field(name="남은 시간", value=cetus_response.json()['timeLeft'] + " 이후 밤으로 바뀝니다",inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def 침공(ctx):
    constructionProgress_response = requests.get(Url + '/constructionProgress')
    embed = discord.Embed(title="침공 정보", color=0x7fa0f4)
    embed.set_image(url="https://i.imgur.com/7A57PSk.png")
    print("시작...")
    print(constructionProgress_response.status_code)
    if constructionProgress_response.status_code == 200:
        embed.add_field(name=":tools:레이저백 건설 현황:tools:", value=constructionProgress_response.json()['razorbackProgress'] + '%', inline=True)
        embed.add_field(name=":tools:포모리안 건설 현황:tools:", value=constructionProgress_response.json()['fomorianProgress'] + '%', inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def 지구(ctx):
    earth_response = requests.get(Url + '/earthCycle')
    embed = discord.Embed(title="지구 정보", color=0x7fa0f4)
    embed.set_image(url="https://i.imgur.com/eGbJ4u1.png")
    print("시작...")
    print(earth_response.status_code)
    if earth_response.status_code == 200:
        if earth_response.json()['isDay'] == True:
            embed.add_field(name="현재 상태", value="낮",inline=True)
        else:
            embed.add_field(name="현재 상태", value="밤", inline=True)
        if earth_response.json()['isDay'] == True:
            embed.add_field(name="남은 시간", value=earth_response.json()['timeLeft'] + " 이후 밤으로 바뀝니다",inline=False)
        else:
            embed.add_field(name="남은 시간", value=earth_response.json()['timeLeft'] + " 이후 낮으로 바뀝니다",inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def 다르보(ctx):
    daily_response = requests.get(Url + '/dailyDeals')
    text=daily_response.text
    data=json.loads(text)
    daily = data[0]
    embed = discord.Embed(title="다르보의 할인 정보", color=0x7fa0f4)
    embed.set_thumbnail(url="https://i.imgur.com/l8rN8O5.png")
    print("시작...")
    print(daily_response.status_code)
    if daily_response.status_code == 200:
        embed.add_field(name="판매 상품", value=daily['item'], inline=False)
        embed.add_field(name="원가**     **", value=str(daily['originalPrice']) + "플래티넘", inline=True)
        embed.add_field(name="할인가**     **", value=str(daily['salePrice']) + "플래티넘", inline=True)
        embed.add_field(name="할인율**     **", value= str(daily['discount']) + "%", inline=True)
        embed.add_field(name="수량**     **", value=str(daily['total']) + "개", inline=True)
        embed.add_field(name="남은 수량**     **", value=str((daily['total'] - daily['sold'])) + '개', inline=True)
        embed.add_field(name="남은 시간", value= daily['eta'] + " 남았습니다", inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def 센티언트(ctx):
    sentient_response = requests.get(Url + '/sentientOutposts')

    FTime = sentient_response.json()['expiry']
    start = FTime.find('T') + 1
    end = FTime.find('.', start)
    Time = FTime[start:end]
    KrTime = 0
    KrTime += (60 * int(Time[0:2]))
    KrTime += int(Time[3:5]) + 780
    Kh = KrTime / 60
    if Kh >= 24:
        Kh -= 24
    Kh = int(Kh)
    Km = KrTime % 60
    TKh = str(Kh)
    if Kh < 10:
        TKh.zfill(2)
    TKm = str(Km)
    TTime = str(Time)
    txt = "KrTime: " + TTime + '\nKh: ' + TKh + "\nKm: " + TKm
    embed = discord.Embed(title="센티언트 함선 정보", color=0x7fa0f4)
    embed.set_image(url="https://i.imgur.com/LN72jmy.png")
    print(sentient_response.status_code)
    if sentient_response.status_code == 200:
        embed.add_field(name="노드", value=sentient_response.json()['mission']['node'], inline=False)
        embed.add_field(name="팩션", value=sentient_response.json()['mission']['faction'], inline=False)
        embed.add_field(name="노드", value=sentient_response.json()['mission']['type'], inline=False)
        embed.add_field(name="남은 시간", value=TTime + "  남았습니다", inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def 출격(ctx):
    sortie_response = requests.get(Url + '/sortie')
    txts = sortie_response.text
    datacnf = json.loads(txts)
    cnf1 = datacnf
    print(sortie_response.status_code)
    if sortie_response.status_code == 200:
        embed = discord.Embed(title="출격 정보", color=0xff8200)
        embed.set_image(url="https://i.imgur.com/SXyjixv.png")
        embed.add_field(name="출격1", value="미션 타입:\n" + cnf1['variants'][0]['missionType'] +
                                          "\n\n특이사항:\n" + cnf1['variants'][0]['modifier'] +
                                          "\n\n노드:\n" + cnf1['variants'][0]['node'], inline=True)
        embed.add_field(name="**     **출격2", value="**     **미션 타입:\n" + cnf1['variants'][1]['missionType'] +
                                          "\n\n특이사항:\n" + cnf1['variants'][1]['modifier'] +
                                          "\n\n노드:\n" + cnf1['variants'][1]['node'], inline=True)
        embed.add_field(name="**     **출격3", value="**     **미션 타입:\n" + cnf1['variants'][2]['missionType'] +
                                          "\n\n특이사항:\n" + cnf1['variants'][2]['modifier'] +
                                          "\n\n노드:\n" + cnf1['variants'][2]['node'], inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def 강철의길(ctx):
    steelPath_response = requests.get(Url + '/steelPath')
    txts= steelPath_response.text
    datacnf = json.loads(txts)
    steelPath = datacnf
    print(steelPath_response.status_code)
    if steelPath_response.status_code == 200:
        embed = discord.Embed(title="강철의 길 훈장", color=0xff8200)
        embed.set_image(url="https://i.imgur.com/bsF25k0.png")
        embed.add_field(name=steelPath['currentReward']['name'],value=str(steelPath['currentReward']['cost'])+ '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][0]['name'],value=str(steelPath['evergreens'][0]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][1]['name'],value=str(steelPath['evergreens'][1]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][2]['name'],value=str(steelPath['evergreens'][2]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][3]['name'],value=str(steelPath['evergreens'][3]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][4]['name'],value=str(steelPath['evergreens'][4]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][5]['name'],value=str(steelPath['evergreens'][5]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][6]['name'],value=str(steelPath['evergreens'][6]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][7]['name'],value=str(steelPath['evergreens'][7]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][8]['name'],value=str(steelPath['evergreens'][8]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][9]['name'],value=str(steelPath['evergreens'][9]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][10]['name'],value=str(steelPath['evergreens'][10]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][11]['name'],value=str(steelPath['evergreens'][11]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][12]['name'],value=str(steelPath['evergreens'][12]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][13]['name'],value=str(steelPath['evergreens'][13]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][14]['name'],value=str(steelPath['evergreens'][14]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][15]['name'],value=str(steelPath['evergreens'][15]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][16]['name'],value=str(steelPath['evergreens'][16]['cost']) + '스틸 에센스', inline=True)
        embed.add_field(name=steelPath['evergreens'][17]['name'],value=str(steelPath['evergreens'][17]['cost']) + '스틸 에센스', inline=True)
        embed.set_footer(text=str(steelPath['remaining']) + " 이후 품목 변경됩니다")
        await ctx.send(embed=embed)


@bot.command()
async def 오브협곡(ctx):
    Orb_response = requests.get(Url + '/vallisCycle')
    embed = discord.Embed(title="캠비온 퇴적지 정보", color=0x0488D0)
    embed.set_image(url="https://i.imgur.com/iGDGW7t.png")
    print("시작...")
    print(Orb_response.status_code)
    if Orb_response.status_code == 200:
        if Orb_response.json()['isWarm'] == False:
            embed.add_field(name="현재 진영", value="추움",inline=True)
            embed.add_field(name="남은 시간", value=Orb_response.json()['timeLeft'] + " 이후 따뜻함으로 변경됩니다",inline=False)
        else:
            embed.add_field(name="현재 진영", value="따뜻함", inline=True)
            embed.add_field(name="남은 시간", value=Orb_response.json()['timeLeft'] + " 이후 추움으로 변경됩니다",inline=False)

        await ctx.send(embed=embed)


""" #개발중
@bot.command()
async def 키티어(ctx):
    Void_response = requests.get(Url + '/voidTrader')
    embed = discord.Embed(title="바로 키티어 정보", color=0xff0000)
    embed.set_image(url="https://i.imgur.com/iGDGW7t.png")
    print("시작...")
    print(Void_response.status_code)
    if Void_response.status_code == 200:
        embed.add_field(name="", value="추움",inline=True)

        await ctx.send(embed=embed)

"""


@bot.command()
async def 근접(ctx, meele):
    meele = re.sub('_', ' ', meele)
    Meele_response = requests.get(QUrl + 'weapons/search/' + meele)
    Mtext = Meele_response.text
    rmswjq = json.loads(Mtext)
    Melle = rmswjq[0]
    print(meele)
    print(Melle)
    if Meele_response.status_code == 200:
        embed = discord.Embed(title=meele + "정보", color=0xceb8ff)
        embed.set_thumbnail(url="https://i.imgur.com/aVby7S2.png")
        embed.add_field(name="무기 이름", value=meele, inline=False)
        embed.add_field(name="공격 속도", value=Melle['attacks'][0]['speed'], inline=False)
        embed.add_field(name="크리티컬 확률", value=str(Melle['attacks'][0]['crit_chance']) + "%", inline=True)
        embed.add_field(name="크리티컬 배수", value=str(Melle['attacks'][0]['crit_mult']) + "배", inline=True)
        embed.add_field(name="상태이상 확률", value=str(Melle['attacks'][0]['status_chance']) + "%", inline=True)
        embed.add_field(name="슬라이드 공격", value=str(Melle['attacks'][0]['slide']), inline=False)
        embed.add_field(name="지면 강타 공격", value=str(Melle['attacks'][0]['slam']['radial']['damage']), inline=True)
        embed.add_field(name="지면 강타 범위", value=str(Melle['attacks'][0]['slam']['radial']['radius']), inline=True)
        embed.add_field(name="무기 속성", value=str(Melle['attacks'][0]['slam']['radial']['element']), inline=False)
        embed.add_field(name="막기 각도", value=str(Melle['blockingAngle']), inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def 원거리(ctx, Cowgun):
    Cowgun = re.sub('_', ' ', Cowgun)
    Cowgun_response = requests.get(QUrl + 'weapons/search/' + Cowgun)
    Ctext = Cowgun_response.text
    rmswjq = json.loads(Ctext)
    CCowgun = rmswjq[0]
    if Cowgun_response.status_code == 200:
        embed = discord.Embed(title=Cowgun + "정보", color=0xffd8e9)
        embed.set_thumbnail(url="https://i.imgur.com/aVby7S2.png")
        embed.add_field(name="무기 이름", value=Cowgun,inline=False)
        embed.add_field(name="치명타 확률", value=str(CCowgun['attacks'][0]['crit_chance']) + "%",inline=True)
        embed.add_field(name="치명타 배수", value=CCowgun['attacks'][0]['crit_mult'],inline=True)
        embed.add_field(name="상태이상 확률", value=str(CCowgun['attacks'][0]['status_chance']) + "%",inline=True)
        embed.add_field(name="무기 정확도", value=str(CCowgun['accuracy']) + "%",inline=True)
        embed.add_field(name="무기 기본 탄약", value=CCowgun['ammo'],inline=True)
        embed.add_field(name="연사력", value=CCowgun['attacks'][0]['speed'],inline=False)
        embed.add_field(name="발사 형식",value=CCowgun['attacks'][0]['shot_type'],inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def 초대(ctx):
    embed=discord.Embed(title='초대 링크', color=0xff8821)
    embed.add_field(name="https://discord.com/oauth2/authorize?client_id=923064131412713552&permissions=8&scope=bot", value="많은 초대 부탁드립니다(__)",inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title='도움말', description='전체 명령어를 보여줍니다', color=0xFF80ED)
    embed.set_author(name="제작: PINK_POMA#6293", url="https://github.com/PINKPOMA/Warframe-Bot-For-Discord",
                     icon_url="https://i.imgur.com/JwsP1Ay.png")
    embed.set_thumbnail(url="https://i.imgur.com/aVby7S2.png")
    embed.add_field(name="침공", value="레이저백과 포모리안의 건설 현황을 보여줍니다\n",inline=False)
    embed.add_field(name="강철의길", value="이번주 강철의 길 훈장의 아이템을 보여줍니다\n",inline=False)
    embed.add_field(name="아이돌론평원", value="아이돌론평원의 현재 주기를 알려줍니다\n",inline=False)
    embed.add_field(name="센티언트", value="센티언트 함선의 위치를 알려줍니다\n",inline=False)
    embed.add_field(name="데이모스", value="데이모스의 현재 주기를 알려줍니다\n",inline=False)
    embed.add_field(name="오브협곡", value="오브협곡의 주기를 알려줍니다\n",inline=False)
    embed.add_field(name="중재", value="현재 중재 상태를 알려줍니다\n",inline=False)
    embed.add_field(name="다르보", value="다르보의 상품을 보여줍니다\n",inline=False)
    embed.add_field(name="지구", value="지구의 시간을 알려줍니다\n",inline=False)
    embed.add_field(name="초대", value="봇 초대 코드를 보내드립니다",inline=False)
    embed.add_field(name="원거리(영어)", value="주,보조 무기의 스탯을 보여줍니다(띄어쓰기 대신 _를 이용해 주세요)",inline=False)
    embed.add_field(name="근접(영어)", value="근접 무기의 스탯을 보여줍니다(띄어쓰기 대신 _를 이용해 주세요)",inline=False)
    await ctx.send(embed=embed)


bot.run(Token)