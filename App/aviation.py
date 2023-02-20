import pprint

import requests
import json
import re
import time







class Aviation(object):
    def __init__(self, search_type='0'):
        self.SearchType = search_type


class Airport(object):
    def __init__(self, ICAO_code, search_type='airport info'):
        self.ICAOCode = ICAO_code
        self.SearchType = search_type

    def GetAirportInfo(self):
        return airinfo_analyzing(airinfo_get(self.ICAOCode))

    def GetRunwayInfo(self):
        return runwayinfo_analyzing(airinfo_get(self.ICAOCode))

    def GetTAFInfo(self):
        return taf_analyzing(taf_get(self.ICAOCode))

    def GetTafRaw(self):
        return taf_raw(taf_get(self.ICAOCode))

    def GetMETARInfo(self):
        return metar_analyzing(metar_get(self.ICAOCode))

    def GetMETARRaw(self):
        return metar_raw(metar_get(self.ICAOCode))


class ATC(Airport):
    def __init__(self, ICAO_code, search_item):
        super().__init__(ICAO_code)
        self.SearchItem = search_item

    def GetATC(self):                                          # 生成对象时传入机场ICAO和查询的ATC类型
        with open('./Json/atc_frequency.json', 'r') as f:
            atc = json.load(f)[f'{self.ICAOCode}'][f'{self.SearchItem}']

        return atc

    @staticmethod
    def GetAirportList():
        return f'机场支持列表：{", ".join(["ZSHC", "ZSPD", "ZSSS", "ZBAA", "ZBAD"])}'


class Plane(object):
    def __init__(self, plane_code='0', plane_type='0'):    # use -
        self.PlaneCode = plane_code
        self.PlaneType = plane_type

    def GetFirstCode(self):
        return self.PlaneType[5:6]

    def GetSecondCode(self):
        return self.PlaneType[6:7]

    def GetType(self):
        return self.PlaneType[0:4]

    def GetCode(self):
        return self.PlaneType[5:]

    def GetEngType(self):
        try:
            with open('./Json/aircraft_code_for_Airbus.json') as f:  # win改\
                Full_code = json.load(f)['full_code']
            with open('./Json/aircraft_code_for_Airbus.json') as f:
                First_code = json.load(f)['first_code']
            with open('./Json/aircraft_code_for_Airbus.json') as f:
                Second_code = json.load(f)['second_code']

            OutList = list()
            OutList.append(f'你查询的机型为：{self.PlaneType}，以下是发动机搭载信息：')
            OutList.append(f'【类别】{self.GetType()}')
            OutList.append(f'【子型号】{First_code[self.GetFirstCode()]}')
            OutList.append(f'【发动机】{Full_code[self.GetType()][self.GetCode()]}')
            OutList.append(f'【发动机提供商】{Second_code[self.GetSecondCode()]}')

            return '\n'.join(OutList)
        except:
            return '解析错误，请检查输入的机型是否正确'

    def GetPlaneInfo(self):
        try:
            url = f'http://winskywebapp.vipsinaapp.com/winsky/index.php/home/PlaneInfo/getById?parameter={self.PlaneCode}'
            response = requests.get(url)
            response.raise_for_status()
            got_info = response.text
            run = True
        except:
            got_info = 'None'
            run = False

        if run:
            with open('./testdoc/planeinfo.json', 'a') as f:   # 写log
                json.dump(got_info, f)

            get_infolist = got_info.splitlines(keepends=False)
            got_infolist = list()
            for line in get_infolist:
                got_infolist.append(line.strip())

            parsinglines = list()
            i = 0
            arange = 5
            long = int(got_infolist[0][44:45])
            for i in range(0, long):
                arange = 5 + (56 * i)
                parsinglines.append(got_infolist[arange])
                for plus in range(10, 47, 4):
                    parsinglines.append(got_infolist[arange + plus])

            output = list()
            output.append(f'共查询到{got_infolist[0][44:45]}架相关联的飞行器')
            for plusline in range(0, long):
                plus2 = 11 * plusline
                output.append(f'【第{parsinglines[plus2][7:8]}架飞行器的信息】')
                output.append(f'【注册号】{parsinglines[plus2 + 1][4:][:-5]}')  # 第16行 去除前4 后5字符
                output.append(f'【运营状态】{parsinglines[plus2 + 2][4:][:-5]}')
                output.append(f'【机型】{parsinglines[plus2 + 3][4:][:-5]}')
                output.append(f'【发动机型号】{parsinglines[plus2 + 4][4:][:-5]}')
                output.append(f'【运营机构】{parsinglines[plus2 + 5][4:][:-5]}')
                output.append(f'【隶属信息】{parsinglines[plus2 + 6][4:][:-5]}')
                output.append(f'【引进日期】{parsinglines[plus2 + 7][4:][:-5]}')
                output.append(f'【首次交付】{parsinglines[plus2 + 8][4:][:-5]}')
                output.append(f'【串号】{parsinglines[plus2 + 9][4:][:-5]}')
                output.append(f'【备注】{parsinglines[plus2 + 10][4:][:-5]}')
                output.append('----分割线----')

            ans = '\n'.join(output)
            return ans


class Route(object):
    def __init__(self, icao_from, icao_to):
        self.ICAOFrom = icao_from
        self.ICAOTo = icao_to

    def GetRoute(self):
        url = 'https://efb.xflysim.com/index.html'
        response = requests.get(url=url)


class Rocket(object):
    def __init__(self, rtype='all'):
        self.Type = rtype

    def GetInfo(self):
        url = 'https://yhcspace.com'
        response = requests.get(url=url)
        response.raise_for_status()
        sep1 = response.text.split(sep='<h5 class="title is-5 yhc-index-section-title mx-3">进行中的发射任务</h5>')
        sep2 = sep1[1].split(sep='</tbody></table></div></section><section class="section"><h5 class="title is-5 yhc-index-section-title mx-3">近期已完成发射任务</h5>')   # 截取待发射任务
        # sep3 = sep2[0].split(sep='</th></tr></thead><tbody>')[2].split(sep='</td><td><p ')  # list
        sep3 = sep2[0].split(sep='</th></tr></thead><tbody>')[2].split(sep='<tr><td><p ')
        sep4 = list()
        sep5 = list()
        sep6 = list()
        ana4 = list()
        ans = list()
        for i in sep3[1:]:
            ana1 = i.split(sep='</p></td><td><p ')
            for n in ana1:
                for m in (n.split(sep='class="my-2">')[1].split(sep='</p></td></tr>')):
                    sep4.append(m)
        for i in sep4:
            ana2 = i.split(sep='</p><p class="my-2 yhc-gray-color">')
            for n in ana2:
                for m in n.split(sep='</p><p'):
                    sep5.append(m)
        for i in sep5:
            ana3 = i.split(sep='<span class="mx-3 yhc-payload-count"')
            for n in ana3:
                sep6.append(n)
        for i in sep6:
            if i != ' ' and i[0:1] != '>' and i != '':
                ana4.append(i)
        ans.append('待发射的任务：')
        for i in range(0, int(len(ana4) / 7)):
            ans.append(f'【载荷】{ana4[0 + 7 * i]}')
            ans.append(f'【发射时间】{ana4[1 + 7 * i]} {ana4[2 + 7 * i]}')
            ans.append(f'【载具】{ana4[3 + 7 * i]}')
            ans.append(f'【发射场】{ana4[5 + 7 * i]} {ana4[4 + 7 * i]}')
            ans.append(f'【发射方】{ana4[6 + 7 * i]}')
            ans.append(f'--------')
        # with open('../testdoc/rocketinfo.txt', 'w') as f:
            # f.write('\n'.join(ans))
        # with open('../testdoc/yhcspace.txt', 'w') as f:
            # f.write('\n'.join(ana4))
        return '\n'.join(ans)

    def GetInfoNew(self):
        url = 'https://yhcspace.com'
        response = requests.get(url=url)
        response.raise_for_status()
        sep1 = response.text.split(sep='<h5 class="title is-5 yhc-index-section-title mx-3">进行中的发射任务</h5>')
        sep2 = sep1[1].split(
            sep='</tbody></table></div></section><section class="section"><h5 class="title is-5 yhc-index-section-title mx-3">近期已完成发射任务</h5>')  # 截取待发射任务
        # sep3 = sep2[0].split(sep='</th></tr></thead><tbody>')[2].split(sep='</td><td><p ')  # list
        sep3 = sep2[0].split(sep='</th></tr></thead><tbody>')[2].split(sep='<tr><td><p ')
        sep4 = list()
        sep5 = list()
        sep6 = list()
        ana4 = list()
        ans = list()
        for i in sep3[1:]:
            ana1 = i.split(sep='</p></td><td><p ')
            for n in ana1:
                for m in (n.split(sep='class="my-2">')[1].split(sep='</p></td></tr>')):
                    sep4.append(m)
        for i in sep4:
            ana2 = i.split(sep='</p><p class="my-2 yhc-gray-color">')
            for n in ana2:
                for m in n.split(sep='</p><p'):
                    sep5.append(m)
        for i in sep5:
            ana3 = i.split(sep='<span class="mx-3 yhc-payload-count"')
            for n in ana3:
                sep6.append(n)
        for i in sep6:
            if i != ' ' and i[0:1] != '>' and i != '':
                ana4.append(i)
        ana5 = list()
        for i in range(0, int(len(ana4) / 7)):
            if not re.search(pattern='\d{1,2}:\d{1,2}', string=f'{ana4[2 + 7 * i]}'):
                ana4.insert(2 + 7 * i, '')
        ans.append('待发射的任务：')
        for i in range(0, int(len(ana4) / 7)):
            ans.append(f'【载荷】{ana4[0 + 7 * i]}')
            ans.append(f'【发射时间】{ana4[1 + 7 * i]} {ana4[2 + 7 * i]}')
            ans.append(f'【载具】{ana4[3 + 7 * i]}')
            ans.append(f'【发射场】{ana4[5 + 7 * i]} {ana4[4 + 7 * i]}')
            ans.append(f'【发射方】{ana4[6 + 7 * i]}')
            ans.append(f'--------')

        # with open('../testdoc/yhcspaceNew.txt', 'w') as f:
            # f.write('\n'.join(ana4))

        return '\n'.join(ans)


class Orbit(object):
    def __init__(self, name='n', group='n', catnr='n', intdes='n', special='n', info='n'):
        self.Name = name
        self.Group = group
        self.CATNR = catnr
        self.INTDES = intdes
        self.Special = special
        self.Info = info

    def GetInfoByName(self):
        url = f'https://celestrak.org/satcat/records.php?NAME={self.Name}&FORMAT=json-pretty'
        response = requests.get(url=url)
        response.raise_for_status()
        GetInfo = json.loads(response.text)    # a list
        return GetInfo

    def GetInfoByGroup(self):
        url = f'https://celestrak.org/satcat/records.php?GROUP={self.Group}&FORMAT=json-pretty'
        response = requests.get(url=url)
        response.raise_for_status()
        GetInfo = json.loads(response.text)    # a list
        return GetInfo


def OrbInfoTrans(GotInfo):  # input a dict output a dict
    for i in GotInfo.keys():
        if i == 'OBJECT_TYPE':
            v = GotInfo['OBJECT_TYPE']
            if v == 'PAY':
                GotInfo['OBJECT_TYPE'] = '载荷'
            elif v == 'R/B':
                GotInfo['OBJECT_TYPE'] = '火箭组件'
            elif v == 'DEB':
                GotInfo['OBJECT_TYPE'] = '废弃组件'
            elif v == 'UNK':
                GotInfo['OBJECT_TYPE'] = '未知'
            else:
                GotInfo['OBJECT_TYPE'] = GotInfo['OBJECT_TYPE']
        elif i == 'OPS_STATUS_CODE':
            v = GotInfo['OPS_STATUS_CODE']
            if v == '+':
                GotInfo['OPS_STATUS_CODE'] = '运行中'
            elif v == '-':
                GotInfo['OPS_STATUS_CODE'] = '未运行'
            elif v == 'P':
                GotInfo['OPS_STATUS_CODE'] = '部分运行'
            elif v == 'B':
                GotInfo['OPS_STATUS_CODE'] = '备份'
            elif v == 'S':
                GotInfo['OPS_STATUS_CODE'] = '备用待激活'
            elif v == 'X':
                GotInfo['OPS_STATUS_CODE'] = '扩展任务'
            elif v == 'D':
                GotInfo['OPS_STATUS_CODE'] = '终止'
            elif v == '?':
                GotInfo['OPS_STATUS_CODE'] = '未知'
            else:
                GotInfo['OPS_STATUS_CODE'] = GotInfo['OPS_STATUS_CODE']
        elif i == 'OWNER':
            v = GotInfo['OWNER']
            if v == 'PRC':
                GotInfo['OWNER'] = '中华人民共和国'
            elif v == 'US':
                GotInfo['OWNER'] = '美国'
            elif v == 'AB':
                GotInfo['OWNER'] = '阿拉伯卫星通信组织'
            elif v == 'ASRA':
                GotInfo['OWNER'] = '奥地利'
            elif v == 'AUS':
                GotInfo['OWNER'] = '澳大利亚'
            elif v == 'CA':
                GotInfo['OWNER'] = '加拿大'
            elif v == 'CHLE':
                GotInfo['OWNER'] = '智利'
            elif v == 'CIS':
                GotInfo['OWNER'] = '独联体/前苏联'
            elif v == 'ESA':
                GotInfo['OWNER'] = '欧空局'
            elif v == 'ESRO':
                GotInfo['OWNER'] = '欧洲空间研究组织'
            elif v == 'EUME':
                GotInfo['OWNER'] = '欧洲气象卫星应用组织'
            elif v == 'EUTE':
                GotInfo['OWNER'] = '欧洲通讯卫星应用组织'
            elif v == 'GER':
                GotInfo['OWNER'] = '德国'
            elif v == 'FR':
                GotInfo['OWNER'] = '法国'
            elif v == 'IM':
                GotInfo['OWNER'] = '国际移动卫星组织'
            elif v == 'IND':
                GotInfo['OWNER'] = '印度'
            elif v == 'ISRA':
                GotInfo['OWNER'] = '以色列'
            elif v == 'ISRO':
                GotInfo['OWNER'] = '印度空间研究组织'
            elif v == 'ISS':
                GotInfo['OWNER'] = '国际空间站'
            elif v == 'ITSO':
                GotInfo['OWNER'] = '国际通信卫星组织'
            elif v == 'JPN':
                GotInfo['OWNER'] = '日本'
            elif v == 'NATO':
                GotInfo['OWNER'] = '北约'
            elif v == 'PRES':
                GotInfo['OWNER'] = '中国/欧空局'
            elif v == 'ROC':
                GotInfo['OWNER'] = '中国台湾'
            elif v == 'UK':
                GotInfo['OWNER'] = '英国'
            else:
                GotInfo['OWNER'] = GotInfo['OWNER']
        elif i == 'LAUNCH_SITE':
            v = GotInfo['LAUNCH_SITE']
        elif i == 'DATA_STATUS_CODE':
            v = GotInfo['DATA_STATUS_CODE']
            if v == 'NEA':
                GotInfo['DATA_STATUS_CODE'] = '无可用要素'
            elif v == 'NIE':
                GotInfo['DATA_STATUS_CODE'] = '无初始要素'
            elif v == 'NCE':
                GotInfo['DATA_STATUS_CODE'] = '无近期要素'
            else:
                GotInfo['DATA_STATUS_CODE'] = '正常'
        elif i == 'ORBIT_CENTER':
            v = GotInfo['ORBIT_CENTER']
            if v == 'AS':
                GotInfo['ORBIT_CENTER'] = '小行星'
            elif v == 'CO':
                GotInfo['ORBIT_CENTER'] = '彗星'
            elif v == 'EA':
                GotInfo['ORBIT_CENTER'] = '地球'
            elif v == 'EL1':
                GotInfo['ORBIT_CENTER'] = '地球第一拉格朗日点（L1）'
            elif v == 'EL2':
                GotInfo['ORBIT_CENTER'] = '地球第二拉格朗日点（L2）'
            elif v == 'EM':
                GotInfo['ORBIT_CENTER'] = '地月引力中心'
            elif v == 'JU':
                GotInfo['ORBIT_CENTER'] = '木星'
            elif v == 'MA':
                GotInfo['ORBIT_CENTER'] = '火星'
            elif v == 'ME':
                GotInfo['ORBIT_CENTER'] = '水星'
            elif v == 'MO':
                GotInfo['ORBIT_CENTER'] = '月球'
            elif v == 'NE':
                GotInfo['ORBIT_CENTER'] = '海王星'
            elif v == 'PL':
                GotInfo['ORBIT_CENTER'] = '冥王星'
            elif v == 'SA':
                GotInfo['ORBIT_CENTER'] = '土星'
            elif v == 'SS':
                GotInfo['ORBIT_CENTER'] = '太阳系外层'
            elif v == 'SU':
                GotInfo['ORBIT_CENTER'] = '太阳'
            elif v == 'UR':
                GotInfo['ORBIT_CENTER'] = '天王星'
            elif v == 'VE':
                GotInfo['ORBIT_CENTER'] = '金星'
            else:
                GotInfo['ORBIT_CENTER'] = GotInfo['ORBIT_CENTER']
        elif i == 'ORBIT_TYPE':
            v = GotInfo['ORBIT_TYPE']
            if v == 'ORB':
                GotInfo['ORBIT_TYPE'] = '轨道'
            elif v == 'LAN':
                GotInfo['ORBIT_TYPE'] = '着陆'
            elif v == 'IMP':
                GotInfo['ORBIT_TYPE'] = 'impact'
            elif v == 'DOC':
                GotInfo['ORBIT_TYPE'] = '对接'
            elif v == 'R/T':
                GotInfo['ORBIT_TYPE'] = 'Roundtrip'
            else:
                GotInfo['ORBIT_TYPE'] = GotInfo['ORBIT_TYPE']
    # 单位补充
    if GotInfo['PERIOD'] == '':
        GotInfo['PERIOD'] = GotInfo['PERIOD']
    else:
        GotInfo['PERIOD'] = f'{GotInfo["PERIOD"]} Min'
    if GotInfo["INCLINATION"] == '':
        GotInfo["INCLINATION"] = GotInfo["INCLINATION"]
    else:
        GotInfo["INCLINATION"] = f'{GotInfo["INCLINATION"]} Deg'
    if GotInfo["APOGEE"] == '':
        GotInfo["APOGEE"] = GotInfo["APOGEE"]
    else:
        GotInfo["APOGEE"] = f'{GotInfo["APOGEE"]} KM'
    if GotInfo["PERIGEE"] == '':
        GotInfo["PERIGEE"] = GotInfo["PERIGEE"]
    else:
        GotInfo["PERIGEE"] = f'{GotInfo["PERIGEE"]} KM'
    if GotInfo["RCS"] == '':
        GotInfo["RCS"] = GotInfo["RCS"]
    else:
        GotInfo["RCS"] = f'{GotInfo["RCS"]} M^2'

    # 检查空值
    for i in GotInfo.keys():
        if GotInfo[i] == '':
            GotInfo[i] = '暂无信息'

    return GotInfo


def OrbitInfoAnaEr(GotInfo):  # input a dict
    OutStr = list()
    OutStr.append(f'【对象名称】{GotInfo["OBJECT_NAME"]}')
    OutStr.append(f'【对象ID】{GotInfo["OBJECT_ID"]}')
    OutStr.append(f'【北美防空司令部识别ID】{GotInfo["NORAD_CAT_ID"]}')
    OutStr.append(f'【对象类型】{GotInfo["OBJECT_TYPE"]}')
    OutStr.append(f'【运行状态】{GotInfo["OPS_STATUS_CODE"]}')
    OutStr.append(f'【所有者】{GotInfo["OWNER"]}')
    OutStr.append(f'【发射日期】{GotInfo["LAUNCH_DATE"]}')
    OutStr.append(f'【发射基地】{GotInfo["LAUNCH_SITE"]}')
    OutStr.append(f'【终止日期】{GotInfo["DECAY_DATE"]}')
    OutStr.append(f'【轨道周期】{GotInfo["PERIOD"]}')
    OutStr.append(f'【轨道倾角】{GotInfo["INCLINATION"]}')
    OutStr.append(f'【远点距离】{GotInfo["APOGEE"]}')
    OutStr.append(f'【近点距离】{GotInfo["PERIGEE"]}')
    OutStr.append(f'【雷达断面】{GotInfo["RCS"]}')
    OutStr.append(f'【数据状态】{GotInfo["DATA_STATUS_CODE"]}')
    OutStr.append(f'【轨道中心】{GotInfo["ORBIT_CENTER"]}')
    OutStr.append(f'【轨道类型】{GotInfo["ORBIT_TYPE"]}')

    return '\n'.join(OutStr)

# a = Orbit(name='fengyun').GetInfoByName()[-1]
# print(OrbitInfoAnaEr(OrbInfoTrans(a)))


# airport_info.py
# GetAirportInfo


def airinfo_get(airport_name):
    try:
        headers = {
            'Authorization': 'BXiGvI3B-vmqqAboBU4Qepfd9mxitY1chTvcgqp-NkA'
        }
        get_url = f'https://avwx.rest/api/station/{airport_name}'
        response = requests.get(get_url, headers=headers)  # get 页面到response.txt
        response.raise_for_status()  # test T or F
        got_dict = json.loads(response.text)  # from json type to python type as a dict
        return got_dict
    except:
        got_dict = {}
        return got_dict


def airinfo_analyzing(adict):
    if adict:
        airinfo_analyzed = list()
        airinfo_analyzed.append(f'【ICAO】{adict["icao"]}')
        airinfo_analyzed.append(f'【IATA】{adict["iata"]}')
        airinfo_analyzed.append(f'【name】{adict["name"]}')
        airinfo_analyzed.append(f'【info】{adict["note"]}')
        airinfo_analyzed.append(f'【纬度】{adict["latitude"]}')
        airinfo_analyzed.append(f'【经度】{adict["longitude"]}')
        airinfo_analyzed.append(f'【标高】{adict["elevation_ft"]}ft({adict["elevation_m"]}m)')
        airinfo_analyzed.append(f'【类型】{adict["type"]}')
        airinfo_analyzed.append('----分隔行----')

        airinfo_output = '\n'.join(airinfo_analyzed)

        runways_info = list()
        runways = adict['runways']  # list
        for runway_dict in runways:  # dict
            runways_info.append(f'跑道：{runway_dict["ident1"]}，航向：{runway_dict["bearing1"]}')
            runways_info.append(f'跑道：{runway_dict["ident2"]}，航向：{runway_dict["bearing2"]}')
            runways_info.append(f'道面长度：{runway_dict["length_ft"]}ft，道面宽度：{runway_dict["width_ft"]}ft')
            if runway_dict['surface'] == 'concrete':
                runways_info.append(f'道面材质：{runway_dict["surface"]}(混凝土)')
            elif runway_dict['surface'] == 'asphalt':
                runways_info.append(f'道面材质：{runway_dict["surface"]}(沥青)')
            else:
                runways_info.append(f'道面材质：')

            runways_info.append(f'跑道灯光：{runway_dict["lights"]}')
            runways_info.append('----分隔行----')

        runwayinfo_output = '\n'.join(runways_info)

        output = f'{airinfo_output}\n{runwayinfo_output}'
        return output

    else:
        output = '信息获取异常，可能是由于网络延迟或输入异常，请检查后重试'
        return output


def runwayinfo_analyzing(adict):
    if adict:
        runways_info = []
        runways = adict['runways']  # list
        for runway_dict in runways:  # dict
            runways_info.append(f'跑道：{runway_dict["ident1"]}，航向：{runway_dict["bearing1"]}')
            runways_info.append(f'跑道：{runway_dict["ident2"]}，航向：{runway_dict["bearing2"]}')
            runways_info.append(f'道面长度：{runway_dict["length_ft"]}ft，道面宽度：{runway_dict["width_ft"]}ft')
            if runway_dict['surface'] == 'concrete':
                runways_info.append(f'道面材质：{runway_dict["surface"]}(混凝土)')
            elif runway_dict['surface'] == 'asphalt':
                runways_info.append(f'道面材质：{runway_dict["surface"]}(沥青)')
            else:
                runways_info.append(f'道面材质：')

            runways_info.append(f'跑道灯光：{runway_dict["lights"]}')
            runways_info.append('----分隔行----')

        runwayinfo_output = '\n'.join(runways_info)
        return runwayinfo_output
    else:
        return '信息获取异常，可能是网络错误'



# METAR and TAF
def metar_get(airport_name):
    try:
        headers = {
            'Authorization': 'BXiGvI3B-vmqqAboBU4Qepfd9mxitY1chTvcgqp-NkA'
        }
        get_url = f'https://avwx.rest/api/metar/{airport_name}'
        response = requests.get(get_url, headers=headers)  # get 页面到response.txt
        response.raise_for_status()  # test T or F
        got_dict = json.loads(response.text)  # from json type to python type as a dict
        return got_dict
    except:
        got_dict = {}
        return got_dict


def taf_get(airport_name):
    try:
        headers = {
            'Authorization': 'BXiGvI3B-vmqqAboBU4Qepfd9mxitY1chTvcgqp-NkA'
        }
        get_url = f'https://avwx.rest/api/taf/{airport_name}'
        response = requests.get(get_url, headers=headers)  # get 页面到response.txt
        response.raise_for_status()  # test T or F
        got_dict = json.loads(response.text)  # from json type to python type as a dict
        return got_dict
    except:
        got_dict = {}
        return got_dict


def taf_raw(adict):
    if adict:
        raw_ans = adict['raw']
        return raw_ans
    else:
        return '信息获取异常，可能是由于网络延迟或输入异常，请检查后重试'


def metar_raw(adict):
    if adict:
        raw_ans = adict['raw']
        return raw_ans
    else:
        return '信息获取异常，可能是由于网络延迟或输入异常，请检查后重试'


def taf_analyzing(adict):
    if adict:
        taf_analyzed = list()

        taf_analyzed.append(f'航站：{adict["station"]}')
        taf_analyzed.append(f'原始TAF信息：{taf_raw(adict)}\n【以下是解析】')
        time = adict['time']
        taf_analyzed.append(f'发布时间：{time["dt"]} UTC')

        forecast_dict_list = adict['forecast']
        forecast_dict = forecast_dict_list[0]

        start_time = forecast_dict['start_time']
        taf_analyzed.append(f'起始时间：{start_time["dt"]} UTC')
        end_time = forecast_dict['end_time']
        taf_analyzed.append(f'终止时间：{end_time["dt"]} UTC')
        taf_analyzed.append(f'飞行条件：{forecast_dict["flight_rules"]}')
        wind_dir = forecast_dict['wind_direction']
        taf_analyzed.append(f'风向：{wind_dir["repr"]}')
        wind_speed = forecast_dict['wind_speed']
        taf_analyzed.append(f'风速：{wind_speed["repr"]}m/s')
        visibility = forecast_dict['visibility']
        taf_analyzed.append(f'能见度：{visibility["repr"]}m')

        clouds = forecast_dict['clouds']
        if clouds:
            clo_dict = clouds[0]
            taf_analyzed.append(f'云高：{clo_dict["altitude"]}，方向：{clo_dict["direction"]}')
        else:
            taf_analyzed.append('没有云数据，没有重要的云')

        max_temp = adict['max_temp']
        min_temp = adict['min_temp']
        taf_analyzed.append(f'最高温度：{max_temp[2:4]}摄氏度，预计在{max_temp[5:7]}日{max_temp[7:9]}时达到')
        taf_analyzed.append(f'最低温度：{min_temp[2:4]}摄氏度，预计在{min_temp[5:7]}日{min_temp[7:9]}时达到')

        taf_analyzed.append('注意：解析仅供参考，请以上文原始TAF信息为准')

        output = '\n'.join(taf_analyzed)

        return output

    else:
        return '信息获取异常，可能是由于网络延迟或输入异常，请检查后重试'


def metar_analyzing(dict):
    if dict:
        metar_analyzed = list()

        metar_analyzed.append(f'航站：{dict["station"]}')
        metar_analyzed.append(f'原始METAR信息：{metar_raw(dict)}\n【以下是解析】')
        time = dict['time']
        metar_analyzed.append(f'发布时间：{time["dt"]} UTC')

        metar_analyzed.append(f'飞行条件：{dict["flight_rules"]}')
        wind_dir = dict['wind_direction']
        metar_analyzed.append(f'风向：{wind_dir["repr"]}度')
        wind_change_list = dict['wind_variable_direction']
        if wind_change_list:
            wind_change_from = wind_change_list[0]['repr']
            wind_change_to = wind_change_list[1]['repr']
            metar_analyzed.append(f'风向变化：从{wind_change_from}度到{wind_change_to}度')
        else:
            metar_analyzed.append('风向变化：无信息')

        wind_speed = dict['wind_speed']
        metar_analyzed.append(f'风速：{wind_speed["repr"]}m/s')

        visibility = dict['visibility']
        if visibility['repr'] == 'CAVOK':
            metar_analyzed.append(f'能见度：{visibility["repr"]}(9999+ m)')
        else:
            metar_analyzed.append(f'能见度：{visibility["repr"]}')

        clouds = dict['clouds']
        if clouds:
            clo_dict = clouds[0]
            metar_analyzed.append(f'云高：{clo_dict["altitude"]}，方向：{clo_dict["direction"]}')
        else:
            metar_analyzed.append('没有云数据，没有重要的云')

        dewpoint_temp = dict['dewpoint']
        temp = dict['temperature']
        metar_analyzed.append(f'环境温度：{temp["repr"]}摄氏度')
        metar_analyzed.append(f'露点温度：{dewpoint_temp["repr"]}摄氏度')

        metar_analyzed.append(f'相对湿度：{dict["relative_humidity"]}')
        altimeter = dict['altimeter']
        metar_analyzed.append(f'气压：{altimeter["value"]}hPa')
        metar_analyzed.append(f'密度高度：{dict["density_altitude"]}')
        metar_analyzed.append(f'压力高度：{dict["pressure_altitude"]}')

        if dict['remarks'] == 'NOSIG':
            metar_analyzed.append(f'天气变化预期：{dict["remarks"]}(预期无变化)')
        else:
            metar_analyzed.append(f'天气变化预期：{dict["remarks"]}')

        metar_analyzed.append('注意：解析仅供参考，请以上文原始METAR信息为准')

        output = '\n'.join(metar_analyzed)

        return output

    else:
        return '信息获取异常，可能是由于网络延迟或输入异常，请检查后重试'


# print(taf_analyzing(taf_get('ZSSS')))

# pprint.pprint(taf_get('ZSSS'))

# pprint.pprint(metar_get('ZSHC'))
# print(metar_analyzing(metar_get('ZSHC')))
# print(metar_analyzing(metar_get('ZSSS')))


def r_get(path):
    try:
        headers = {
            'Authorization': 'BXiGvI3B-vmqqAboBU4Qepfd9mxitY1chTvcgqp-NkA'
        }
        get_url = f'https://avwx.rest/api/path/station?route={path}&distance=5'
        response = requests.get(get_url, headers=headers)  # get 页面到response.txt
        response.raise_for_status()  # test T or F
        got_dict = json.loads(response.text)  # from json type to python type as a dict
        return got_dict
    except:
        got_dict = {}

# pprint.pprint(r_get('KMCO%3BORL%3BKDAB'))


# route
# Test version 0.1.0
# route storage dict
route_storage = {'data version': '2109',
                 'ZBAA TO ZSSS': {'route': 'ZBAA SID ELKUR W40 YQG W142 DALIM A593 VMB W161 SASAN STAR ZSSS',
                                  'FL': '9500m(FL311)、10100m(FL331)、10700m(FL351)',
                                  'distance': '航路里程 613.93 nm。直飞航向 155，直飞里程 580.00 nm。'},
                 'ZBAA TO ZSPD': {'route': 'ZBAA SID ELKUR W40 YQG W142 DALIM A593 VMB W161 SASAN STAR ZSPD',
                                  'FL': '9500m(FL311)、10100m(FL331)、10700m(FL351)',
                                  'distance': '航路里程 636.93 nm。直飞航向 153，直飞里程 592.00 nm'},
                 'ZBAA TO ZSHC': {'route': 'ZBAA SID ELKUR W40 YQG W142 DALIM A593 DPX A470 IGRAT STAR ZSHC',
                                  'FL': '9500m(FL311)、10100m(FL331)、10700m(FL351)',
                                  'distance': '航路里程 636.25 nm。直飞航向 161，直飞里程 619.00 nm。'},
                 'ZSSS TO ZBAA': {'route': 'ZSSS SID SASAN W161 VMB A593 DALIM W157 AVBOX STAR ZBAA',
                                  'FL': '9200m(FL301)、9800m(FL321)、10400m(FL341)',
                                  'distance': '航路里程 620.88 nm。直飞航向 338，直飞里程 580.00 nm。'},
                 'ZSPD TO ZBAA': {'route': 'ZSPD SID ODULO B221 XDX W174 TAO W103 JDW V89 DOVIV W55 DUMAP STAR ZBAA',
                                  'FL': '9200m(FL301)、9800m(FL321)、10400m(FL341)',
                                  'distance': '航路里程 636.93 nm。直飞航向 153，直飞里程 592.00 nm。'},
                 'ZSHC TO ZBAA': {'route': 'ZSHC SID NIVIK W135 DOGVI A470 DPX A593 DALIM W157 AVBOX STAR ZBAA',
                                  'FL': '9200m(FL301)、9800m(FL321)、10400m(FL341)',
                                  'distance': '航路里程 636.25 nm。直飞航向 161，直飞里程 619.00 nm'}}


def route_get(fromto):
    try:
        info_dict = route_storage[f'{fromto}']
        rout_info = list()
        rout_info.append(f'【数据版本】{route_storage["data version"]}')
        rout_info.append(f'【航路信息】{info_dict["route"]}')
        rout_info.append(f'【高度层】{info_dict["FL"]}')
        rout_info.append(f'【里程】{info_dict["distance"]}')
        rout_info.append(f'----以下是起降机场有关信息----')
        rout_info.append(f'【起飞机场TAF】{taf_raw(taf_get(fromto[0:4]))}')
        rout_info.append(f'【目的机场TAF】{taf_raw(taf_get(fromto[8:12]))}')
        rout_info.append(f'【起飞机场跑道】{runwayinfo_analyzing(airinfo_get(fromto[0:4]))}')
        rout_info.append(f'【目的机场跑道】{runwayinfo_analyzing(airinfo_get(fromto[8:12]))}')
        output = '\n'.join(rout_info)
        return output
    except:
        return '解析异常或网络异常，请检查输入后重试'


# air performance
# For 737-800W CFM56-7B26 KG M FAA CATC/N FCOM code PI90

# 起飞速度 干跑道条件 无风修正 坡度修正 最大起飞推力（MTT）
speed_dict = {'40': {'FLAPS 1': 'V1:105 VR:106 V2:125', 'FLAPS5': 'V1:101 VR:102 V2:120'}}  # key：weight value：flaps

w40f1 = 'V1:105 VR:106 V2:125'


# plane info
def plane_info(plane_code):
    try:
        url = f'http://winskywebapp.vipsinaapp.com/winsky/index.php/home/PlaneInfo/getById?parameter={plane_code}'
        response = requests.get(url)
        response.raise_for_status()
        got_info = response.text
        run = True
    except:
        got_info = 'None'
        run = False

    if run:
        filename1 = 'plane info.txt'
        with open(filename1, 'w') as textobjw:
            textobjw.write(got_info)
        with open(filename1) as textobjr:
            lines = textobjr.readlines()

        outlines = []
        for line in lines:
            outline = line.strip()
            outlines.append(outline)
        outlines_text = '\n'.join(outlines)
        filename2 = 'outlines.txt'
        with open(filename2, 'w') as textobja:
            textobja.write(outlines_text)

        parsinglines = []
        i = 0
        arange = 5
        long = int(outlines[0][44:45])
        for i in range(0, long):
            arange = 5 + (56 * i)
            parsinglines.append(outlines[arange])
            for plus in range(10, 47, 4):
                parsinglines.append(outlines[arange + plus])

        parsinglines_text = '\n'.join(parsinglines)
        filename3 = 'parsinglines.txt'
        with open(filename3, 'w') as textobj4:
            textobj4.write(parsinglines_text)

        output = []
        output.append(f'共查询到{outlines[0][44:45]}架相关联的飞行器')
        for plusline in range(0, long):
            plus2 = 11 * plusline
            output.append(f'【第{parsinglines[plus2][7:8]}架飞行器的信息】')
            output.append(f'【注册号】{parsinglines[plus2 + 1][4:][:-5]}')  # 第16行 去除前4 后5字符
            output.append(f'【运营状态】{parsinglines[plus2 + 2][4:][:-5]}')
            output.append(f'【机型】{parsinglines[plus2 + 3][4:][:-5]}')
            output.append(f'【发动机型号】{parsinglines[plus2 + 4][4:][:-5]}')
            output.append(f'【运营机构】{parsinglines[plus2 + 5][4:][:-5]}')
            output.append(f'【隶属信息】{parsinglines[plus2 + 6][4:][:-5]}')
            output.append(f'【引进日期】{parsinglines[plus2 + 7][4:][:-5]}')
            output.append(f'【首次交付】{parsinglines[plus2 + 8][4:][:-5]}')
            output.append(f'【串号】{parsinglines[plus2 + 9][4:][:-5]}')
            output.append(f'【备注】{parsinglines[plus2 + 10][4:][:-5]}')
            output.append('----分割线----')

        ans = '\n'.join(output)
        return ans

    else:
        return '解析异常或网络延迟，请检查输入稍后重试'


def loading():
    while True:
        data_time = time.strftime("%Y-%m-%d,%H:%M:%S")
        rocket_info = Rocket().GetInfoNew()   # Str
        info_list = (data_time, rocket_info)
        url_macos = '../Json/Rocket.json'
        url_win = 'C:\\Users\\Administrator\\01\\Json\\Rocket.json'
        with open(url_win, 'w') as f:
            json.dump(info_list, f)
        print('Rocket Information Get OK')
        time.sleep(21600)





