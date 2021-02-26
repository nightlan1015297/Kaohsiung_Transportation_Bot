from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent,TextMessage,TextSendMessage,LocationMessage,LocationSendMessage)

from hashlib import sha1
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime,time
import hmac
import base64
import requests
import json
import numpy as np
app = Flask(__name__)


line_bot_api = LineBotApi(LINE_API_KEY)
handler = WebhookHandler(HANDLER_KEY)

with open('Bicycle_location_detail.json','r',encoding = 'utf8') as load_f:
    Bicycle_Station_Location_detail_Json= json.load(load_f)
Bicycle_Station_Location_array =np.array([[22.680599, 120.297466],
 [22.630663, 120.357928],
 [22.632193, 120.301736],
 [22.618946, 120.2778],
 [22.622261, 120.275466],
 [22.622573, 120.289162],
 [22.62947, 120.295631],
 [22.623751, 120.300808],
 [22.6058, 120.308565],
 [22.619958, 120.311451],
 [22.625204, 120.319704],
 [22.624937, 120.341108],
 [22.630995, 120.310233],
 [22.64818, 120.303512],
 [22.658611, 120.302691],
 [22.676996, 120.306484],
 [22.614348, 120.30466],
 [22.665982, 120.303109],
 [22.627638, 120.301264],
 [22.627252, 120.310898],
 [22.634204, 120.305899],
 [22.598783, 120.313393],
 [22.627368, 120.333654],
 [22.611981, 120.304955],
 [22.628955, 120.328987],
 [22.627712, 120.29068],
 [22.660913, 120.310678],
 [22.633976, 120.285852],
 [22.65226, 120.303892],
 [22.64921, 120.309919],
 [22.610203, 120.299343],
 [22.595861, 120.304928],
 [22.664695, 120.31018],
 [22.629767, 120.318253],
 [22.608549, 120.316435],
 [22.61362, 120.313978],
 [22.624053, 120.290406],
 [22.622587, 120.283159],
 [22.605003, 120.30488],
 [22.62079, 120.293598],
 [22.624337, 120.26566],
 [22.639878, 120.322807],
 [22.664363, 120.296876],
 [22.657992, 120.296334],
 [22.655918, 120.289135],
 [22.625133, 120.362708],
 [22.625063, 120.363416],
 [22.62594, 120.355828],
 [22.624113, 120.356491],
 [22.619844, 120.348068],
 [22.625313, 120.348543],
 [22.62974, 120.344351],
 [22.653562, 120.349281],
 [22.564789, 120.353658],
 [22.566265, 120.372176],
 [22.565198, 120.358618],
 [22.600957, 120.32557],
 [22.637937, 120.298753],
 [22.645214, 120.307123],
 [22.650571, 120.295722],
 [22.662922, 120.312202],
 [22.671912, 120.304348],
 [22.690574, 120.292463],
 [22.700928, 120.302471],
 [22.701989, 120.29259],
 [22.718406, 120.306221],
 [22.721531, 120.296355],
 [22.730211, 120.32053],
 [22.752774, 120.331578],
 [22.744869, 120.317899],
 [22.780613, 120.300722],
 [22.797512, 120.294591],
 [22.6182, 120.266181],
 [22.679928, 120.292102],
 [22.715581, 120.290213],
 [22.554138, 120.34757],
 [22.665096, 120.321665],
 [22.67117, 120.320951],
 [22.659621, 120.324749],
 [22.650378, 120.325634],
 [22.656168, 120.322775],
 [22.569418, 120.343726],
 [22.693598, 120.295864],
 [22.677816, 120.299942],
 [22.686674, 120.308278],
 [22.688085, 120.297361],
 [22.579527, 120.329016],
 [22.573815, 120.320044],
 [22.57217, 120.317475],
 [22.61385, 120.318304],
 [22.589048, 120.322925],
 [22.633129, 120.323558],
 [22.616351, 120.324878],
 [22.615717, 120.299094],
 [22.650698, 120.3488],
 [22.631456, 120.303227],
 [22.631089, 120.304429],
 [22.635323, 120.313318],
 [22.732634, 120.284253],
 [22.727406, 120.292047],
 [22.655851, 120.299933],
 [22.608252, 120.272264],
 [22.666014, 120.303262],
 [22.647866, 120.303345],
 [22.649398, 120.309879],
 [22.624214, 120.300923],
 [22.620733, 120.293601],
 [22.614432, 120.304416],
 [22.620097, 120.311969],
 [22.629797, 120.318221],
 [22.625373, 120.319594],
 [22.608306, 120.316265],
 [22.608217, 120.272334],
 [22.61302, 120.343262],
 [22.588154, 120.32193],
 [22.65495, 120.283089],
 [22.685999, 120.314104],
 [22.801439, 120.357113],
 [22.658443, 120.346107],
 [22.639959, 120.346333],
 [22.643133, 120.339539],
 [22.642492, 120.333667],
 [22.663888, 120.315002],
 [22.562743, 120.335459],
 [22.565069, 120.338391],
 [22.605399, 120.395458],
 [22.60608, 120.427392],
 [22.633877, 120.392021],
 [22.621312, 120.390423],
 [22.604022, 120.391128],
 [22.68838, 120.307605],
 [22.682814, 120.312075],
 [22.680077, 120.321723],
 [22.786133, 120.295002],
 [22.785084, 120.290891],
 [22.790537, 120.296173],
 [22.784278, 120.297605],
 [22.593917, 120.316238],
 [22.593092, 120.307349],
 [22.601729, 120.291757],
 [22.811389, 120.343875],
 [22.624979, 120.31697],
 [22.631218, 120.338583],
 [22.625217, 120.308457],
 [22.731132, 120.317048],
 [22.726234, 120.302495],
 [22.614189, 120.343893],
 [22.659623, 120.296881],
 [22.619285, 120.284972],
 [22.567722, 120.362808],
 [22.672155, 120.311353],
 [22.879024, 120.211033],
 [22.648561, 120.353384],
 [22.630171, 120.3441],
 [22.655859, 120.351552],
 [22.662492, 120.341789],
 [22.668333, 120.34591],
 [22.623122, 120.322092],
 [22.570005, 120.335748],
 [22.60411, 120.302531],
 [22.61211, 120.323489],
 [22.610606, 120.302104],
 [22.614312, 120.360651],
 [22.614298, 120.336654],
 [22.624523, 120.371078],
 [22.61274, 120.34035],
 [22.622089, 120.32909],
 [22.627568, 120.296977],
 [22.636053, 120.343413],
 [22.672199, 120.331266],
 [22.663383, 120.326475],
 [22.653075, 120.31874],
 [22.680522, 120.305831],
 [22.680827, 120.317428],
 [22.674425, 120.286455],
 [22.695437, 120.28737],
 [22.663878, 120.306713],
 [22.651728, 120.276293],
 [22.703625, 120.345135],
 [22.590139, 120.285186],
 [22.871535, 120.19391],
 [22.687264, 120.289478],
 [22.577509, 120.322038],
 [22.739188, 120.305053],
 [22.617966, 120.305523],
 [22.727122, 120.255518],
 [22.67706, 120.306536],
 [22.650448, 120.357777],
 [22.62044, 120.277112],
 [22.620269, 120.277544],
 [22.90801, 120.17704],
 [22.625742, 120.26535],
 [22.646565, 120.318354],
 [22.583112, 120.320345],
 [22.651675, 120.302047],
 [22.620335, 120.360163],
 [22.642316, 120.299238],
 [22.722583, 120.316493],
 [22.65077, 120.287537],
 [22.68113, 120.313956],
 [22.620589, 120.279365],
 [22.620987, 120.270048],
 [22.595525, 120.321994],
 [22.642476, 120.308711],
 [22.659491, 120.288197],
 [22.676383, 120.312624],
 [22.66754, 120.2853],
 [22.67081, 120.289827],
 [22.691503, 120.316115],
 [22.65838, 120.30641],
 [22.62665, 120.37977],
 [22.62879, 120.26266],
 [22.63087, 120.28844],
 [22.60557, 120.31267],
 [22.7446, 120.33132],
 [22.65713, 120.30899],
 [22.66633, 120.32522],
 [22.62275, 120.29926],
 [22.756118, 120.305734],
 [22.603362, 120.302008],
 [22.603152, 120.302115],
 [22.73629, 120.33146],
 [22.603916, 120.391096],
 [22.7175, 120.29495],
 [22.62636, 120.2867],
 [22.635532, 120.29494],
 [22.68124, 120.28281],
 [22.56442, 120.33113],
 [22.668842, 120.309522],
 [22.6811, 120.3518],
 [22.670838, 120.324777],
 [22.73261, 120.33512],
 [22.65436, 120.30887],
 [22.640612, 120.332317],
 [22.610988, 120.33605],
 [22.67661, 120.34195],
 [22.484821, 120.399454],
 [22.61557, 120.35475],
 [22.62748, 120.35976],
 [22.631881, 120.36827],
 [22.6675, 120.29223],
 [22.623279, 120.271726],
 [22.64536, 120.34127],
 [22.56657, 120.3455],
 [22.59456, 120.35774],
 [22.60311, 120.32405],
 [22.68662, 120.31233],
 [22.797096, 120.29073],
 [22.6106, 120.302066],
 [22.60933, 120.3131],
 [22.60614, 120.33876],
 [22.60223, 120.35337],
 [22.64632, 120.37048],
 [22.599155, 120.319892],
 [22.818683, 120.226385],
 [22.76143, 120.2347],
 [22.690106, 120.337416],
 [22.66458, 120.4272],
 [22.66209, 120.4268],
 [22.65679, 120.42084],
 [22.656953, 120.420897],
 [22.623066, 120.269875],
 [22.64616, 120.278703],
 [22.654522, 120.295648],
 [22.67407, 120.29581],
 [22.69372, 120.30194],
 [22.78448, 120.27589],
 [22.76102, 120.30996],
 [22.73764, 120.304188],
 [22.64049, 120.36525],
 [22.61514, 120.34825],
 [22.62101, 120.32574],
 [22.58682, 120.31382],
 [22.64518, 120.37258],
 [22.63057, 120.35826],
 [22.61092, 120.34361],
 [22.6091, 120.33057],
 [22.646569, 120.289018],
 [22.625938, 120.301552],
 [22.60517, 120.30069],
 [22.607155, 120.359701],
 [22.79462, 120.27131],
 [22.71917, 120.285997],
 [22.620423, 120.29733],
 [22.6128, 120.2921],
 [22.62489, 120.32405],
 [22.63627, 120.35689],
 [22.581963, 120.350604],
 [22.581987, 120.350347],
 [22.52183, 120.39078],
 [22.627848, 120.279371],
 [22.81849, 120.26778],
 [22.5582, 120.33553],
 [22.59713, 120.35371],
 [22.79291, 120.29933],
 [22.619799, 120.288904],
 [22.59634, 120.31537],
 [22.641065, 120.303608],
 [22.640956, 120.303587],
 [22.674512, 120.293163],
 [22.652038, 120.281111],
 [22.617278, 120.293559],
 [22.666149, 120.286779],
 [22.659107, 120.302831],
 [22.853701, 120.262653],
 [22.685818, 120.324581],
 [22.638699, 120.315209],
 [22.637178, 120.325194],
 [22.642038, 120.280524]])

Change_Richmenu_Headers = {'Authorization':'Bearer {LINE_API_KEY}'
,'Content-Type':'application/json'}

RICHMENU_HOME_PAGE           ='RICHMENU_HOME_PAGE_KEY'
RICHMENU_for_KRTC_REDorORANGE='RICHMENU_for_KRTC_REDorORANGE_KEY'
RICHMENU_for_KRTC_RED_Page00 ='RICHMENU_for_KRTC_RED_Page00_KEY'
RICHMENU_for_KRTC_RED_Page01 ='RICHMENU_for_KRTC_RED_Page01_KEY'
RICHMENU_for_KRTC_ORG_Page00 ='RICHMENU_for_KRTC_ORG_Page00_KEY'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }



def Get_KRTC_Data(target):    
    a = Auth(KRTC_AUTH_KEY_1,KRTC_AUTH_KEY_2)
    url = "https://ptx.transportdata.tw/MOTC/v2/Rail/Metro/LiveBoard/KRTC?$format=JSON"
    updatetime = time()
    response = requests.get(url, headers= a.get_auth_header())
    Jsondata = json.loads(response.text)
    Cache = []
    for data in Jsondata:
        if data['StationName']['En']==target:
            Cache.append(data)
    Opt_list = []
    for data in Cache:
        string = '[{}站]：下班車往  {:　^３s}  還要等 {} 分鐘'.format(data['StationName']['Zh_tw'],data['DestinationStationName']['Zh_tw'],data['EstimateTime'])
        Opt_list.append(string)
    Opt_list.append('[更新時間]： '+Jsondata[0]['UpdateTime'])
    Opt = '\n'.join(Opt_list)
    return Opt


def Change_Richmenu_data(menu_id,userid):
    string = '{"richMenuId":' + '"'+menu_id+'"'+","+'"userIds":' + "[" + '"'+userid+'"'+"]"+"}"
    return  string




@app.route("/")
def home():
    return '404 ERROR'


@app.route("/moniter", methods=['POST'])
def moniter():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text[0] == "/":
        user_id = str(event.source.user_id)
        if event.message.text =="/HOME":
            requests.post('https://api.line.me/v2/bot/richmenu/bulk/link',headers=Change_Richmenu_Headers,data=Change_Richmenu_data(RICHMENU_HOME_PAGE,user_id))
            line_bot_api.reply_message(event.reply_token,TextSendMessage("回首頁！"))
        if event.message.text =="/MRT":
            requests.post('https://api.line.me/v2/bot/richmenu/bulk/link',headers=Change_Richmenu_Headers,data=Change_Richmenu_data(RICHMENU_for_KRTC_REDorORANGE,user_id))
            line_bot_api.reply_message(event.reply_token,TextSendMessage("選擇路線！"))
        if event.message.text =="/RED":
            requests.post('https://api.line.me/v2/bot/richmenu/bulk/link',headers=Change_Richmenu_Headers,data=Change_Richmenu_data(RICHMENU_for_KRTC_RED_Page00,user_id))
            line_bot_api.reply_message(event.reply_token,TextSendMessage("選擇站名！"))
        if event.message.text =="/RED01":
            requests.post('https://api.line.me/v2/bot/richmenu/bulk/link',headers=Change_Richmenu_Headers,data=Change_Richmenu_data(RICHMENU_for_KRTC_RED_Page01,user_id))
            line_bot_api.reply_message(event.reply_token,TextSendMessage("選擇站名！"))
        if event.message.text =="/ORANGE":
            requests.post('https://api.line.me/v2/bot/richmenu/bulk/link',headers=Change_Richmenu_Headers,data=Change_Richmenu_data(RICHMENU_for_KRTC_ORG_Page00,user_id))
            line_bot_api.reply_message(event.reply_token,TextSendMessage("選擇站名！"))
        if event.message.text[:6] =="/FUNC0":
            reply = Get_KRTC_Data(event.message.text[7:])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
        if event.message.text =="/info":
            line_bot_api.reply_message(event.reply_token,TextSendMessage('嗨！我是Dim，請多指教:D'))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    latitude = event.message.latitude
    longitude = event.message.longitude
    target = np.array([latitude,longitude])
    Cache = Bicycle_Station_Location_array-target
    result = []
    for dat in Cache :
        result.append(np.dot(dat,dat))
    min_index = result.index(min(result))
    station_result = Bicycle_Station_Location_detail_Json[min_index]
    a = Auth(KRTC_AUTH_KEY_1,KRTC_AUTH_KEY_2)
    url = 'https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Kaohsiung?$format=JSON'
    response = requests.get(url, headers= a.get_auth_header())
    Jsondata = json.loads(response.text)
    Rent_avalible = Jsondata[min_index]['AvailableRentBikes']
    Return_avalible = Jsondata[min_index]['AvailableReturnBikes']
    message = LocationSendMessage(title="離你最近的CityBike在 {} \n目前可借 {} 輛 \n目前可還 {} 輛 ".format(station_result['StationName']['Zh_tw'],Rent_avalible,Return_avalible),address=station_result['StationAddress']['Zh_tw'],latitude=station_result['StationPosition']['PositionLat'],longitude=station_result['StationPosition']['PositionLon'])
    line_bot_api.reply_message(event.reply_token,message)

if __name__ == "__main__":
    app.run()
    