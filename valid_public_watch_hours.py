import os

import pickle

from pprint import pprint

import subprocess

# from pydebugger.debug import debug
from datetime import datetime
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    start_date = '2023-07-17'
    end_date = '2023-07-23'
    git_commit = subprocess.run(["git log | head -n 1"], stdout=subprocess.PIPE, text=True, shell=True).stdout
    output_file_path = f'output/stats_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.txt'
    add_to_stats_file(
        f"""start_date: {start_date}
end_date: {end_date}
git_commit: {git_commit}""",
        output_file_path
    )

    youtube = get_youtube()

    youtube_analytics = get_youtube_for_analytics()

    # do_test_thing(youtube_analytics)

    video_ids = get_all_video_ids_for_my_channel(youtube)
    add_to_stats_file(
        f'video_ids length: {len(video_ids)}',
        output_file_path
    )

    # video_ids = ['he2JBiIaSrw', 'B1td1aEja6Y', 'ceKTPNM6ERI', 'IOzZawfnTyk', 'N7qa8K-rhQY', 'uqBMz2m0ppI', '_g2lx_igDQk', '0u_XFExr-ok', 'U2E_FkLLrmo', 'nAXKQBokqWw', 'SV2j6uzP3pc', '_gAQX72Du9U', 'v3Kr22Y4mW4', '_RKigSPdF3Y', 'cCXjDM4Phqs', 'gb1kuBo57_Q', 'Gz3S_qf3Ub4', 'uFOksjM5QB8', '7LXH5nArL0o', 'zbbDL5wPfXI', 'Z82C8jPSIac', 'L9X-jvk3uMk', 'OHR9sBV_Odg', 'pxtuwaKnwLQ', '2RyUb03JxTM', '0VjpGPu4exQ', 'BtySKA5aIjU', 'AgM_meE8ncA', 'njq-sMdSNXs', '-GjNFBEpMl8', 'u2msyE_Xmts', 'oD0Y1UxEc2U', '2u61_W3Fg7o', '2ndBrRNVpzA', 'FO5OKw_enyg', 'HhDYYQK4p7c', 'MGGSQlPPc58', 'P12D2swA2NI', 'Sq_6AuPa_eE', 'ZP_ZjLN-RG8', 'aMrvhDXQ8b4', 'g4oWu11-7Ms', '_XnASY7ebRI', 'ShDU8sdb3OM', 'cU6_3dh9wx8', 'ESiAJ4VHsQI', '819T5hsQH-I', 'etL-7Nc6vM0', 'H4U79qWXF5Y', '3cTEt5HOHDM', 'GtNsLBLOB4M', 'SXuzwQm6wKI', 'SfjB7DawYcI', 'xdxrUG0oWPA', 'MppRhpD6Ga8', 'SfqWkh1XKw0', '2SQ5IVqxhqw', 'RYxaKMlZm20', 'roHyrenq0Kc', 'IGb5se9MJYk', 'jLL513Bwggs', 'yjMdGcF_ze8', 'sy-Shqj-tPE', 'khFB4PwZxJU', '33pHAof8DDA', 'jcPk1CfFS9w', '8MTuxM0SNDw', 'LNipM5a2KQU', '4dj01cSHIpo', 'F0OftsCKATA', 'a1XnaWrA-2U', '80tv4j052H4', 'guHNT6lAa5I', '6xi0Uw9XU_U', 'R_4es5v8gT0', 'WiLn7Dk44Xs', '4OcatjEnzgs', 'ffIH5rOAK70', '_sIGf3YWUfA', 'qk5G2rYNL-Y', '5SJ1RGIbM7U', 'YMNS8BvWJwM', 'AZAUC9ozY1A', 'DHx020oG5ig', 'Py-vHN0LJk8', 'budNrwsqNw8', '9hIOrV30n9o', 'o4pxpWt-v3g', 'SkAWGx3pRdc', 'jgGRqKt2nZk', '4v-lVyx0r2A', 'UHZgQXXkAnQ', '6VKtx1PyXh0', 'A7D04dl0Sy0', 'yMGa4uWFPO4', 'Kqp096g_vcI', 'IZZ7oT30VY4', 'tKrW_51FK1Q', 'Z1MtZKU9fRg', 'OXMZJT3Jf5M', 'GoGpqXcJYP0', 'Ub-z6LcW-iU', 'VccfBSzBoxg', 'FWLhYoK3xFE', '4fleXHCEtpI', 'R11VmoNCE2I', 'oYWbT1Fuz18', 'aoeitKUVfeU', 'Vw04dXbBvqM', 'gReMDBLkwIk', '5HtrTsn8OkY', 'EgHksqIwlyQ', 'yzxG4OwAkqc', 'mnkSlUHu4RY', 'pkHlYQRnPUE', 'NVEnj8kAIwQ', 'ItOaJpfDq5w', 'j7Qo37PoOhM', 'GGZYKlIcS24', 'fGzLq6Ws0S8', 'G37aeuomwII', 'NrjL0tpOym4', 'SWffqpmsFW0', '1kPr1na1xtE', 'UBegb8Eg21Q', 'ysmuiTiJUo0', 'jfs0mubVz7A', 'Cj2Rl2c6bjo', '7iC-KH7NFbA', 'X1tpgkgy02M', 'IpC-WsRyINQ', 'YlL7rrEYlF0', 'jM6-txG11Os', 'cBBlsMBRJ-0', 'gQFF_HhOnKw', 'gLqig6DFj0s', 'mYkyWl9dCeI', 'XM1j7cAX9II', '_RtbiqUqqIk', 'B4-5wheRDwQ', 'UnXNbpfC4r8', '8YV4Q6cbguY', 'fwtJgewYgOo', 'rsJDW1nUl2s', 'Ple-MsFilOU', 'u2SYaRFxLx0', 'bTLQmnX1vmg', 'bkg8ch3GV90', 'K8vM6dfisuE', 'P4MSpd-ENog', '5ryf3SwNADI', 'oostn1TQ6t8', 'ru8ZxoCiJeg', 'gpTnD6a3wqw', 'xwmkDg2JKy0', 'xJTvITUQ_is', 'bKINNP1b6zE', 'L9Lk08nKKVY', 'U5rRPHoMhkM', 'Ydx6DzrEp8w', 'wMCs2Py-Ldk', 'GApWG1N0tFc', 'UA3I3Rvj09w', 'Ms0CDpaDoIo', 'IfAElOseOiE', 'tWx9rLZDkrE', '7qcvJK1NyEM', 'j8QWfpLL02o', 'uXo8oaN5dHg', 'E_Lc7TCq4Ew', 'Wlmth0b8XkU', 'GZPguS75TFE', 'xvy8sNQ7dFE', 'YU_c22ZpTGM', 'Haf9NKAJlqM', 'fQNgVGy9eFc', 'GMFh9woyOv0', 'SHvzrcDs0pg', '6byaa1yQQk8', 'e8ZoWonhdOU', 'QKiXaXbU9wk', 'tbEtC0sgWi0', 'Iog5-hx9JYw', '2X2-tJmZ5Og', 'PzElD9BNuns', '-dIadOxzpqs', 'hnE-Ux_X_b8', 'QFhWS4qh2XY', 'ua7WHf-Kmek', 'R0J-MKjDnLg', 'KaW4NwIiBGk', 'HUdBeoKuC60', '4XVb8cFbRBs', 'hWhdGq6CGYM', 'HjlQWyvYNZM', '65LU1MNBCnA', 'snJ5Z5hU0uM', 'LZ9fx3uoZmc', 'MkhBRKnXVvY', 'VKzemMxXdXg', 'TKpsFGwCLj4', '46NAK_IgAJ0', 'iAAPu7l5sQA', '0HY0d_HZ2t8', 'OvIDo5OWyyE', 'vGuoOPOFHVM', '0-bWyvD6aks', 'KdjXaFSRGC8', 'lQoU6_uXa64', '5gmFZTu1vMM', 'TjJVUgM4iN0', 'fL6veYr1Em4', 'OwPoEj9YW8U', 'SapRuHCSj6k', 'VQ99g5jPNCE', 'L50omm2cbf0', 'Izkt_sc8-Io', 'fHPHVvrvpLk', 'Ypz05RTpeDg', 'BSXTkxHXF58', 'KAwmnGuZzWk', 'dRy8Y3hZE8c', 't7O8Ai9owPo', '5Ks452lSg4w', 'Fpy1XR2Pcag', 'pELoBG9aZxY', 'plq8aD9o08g', 'IIThxk9tUa8', 'SQ9Bqre631w', 'UJJOlUg4a4A', 'vkOCX8WHTfg', 'xNMXbfJ5CLo', 'U4k4JKgVx7w', '8ly2yriqP7I', 'QQHjeSxitEw', 'm9KGXrOeUNA', 'e8t62Oz1fqs', 'e3n31VpF9dI', 'HoGOye_Rt50', '695z2ScdeXY', 'e0h2NpiTsP0', 'Z2Peak8nkuY', 'odaPRfO2AGQ', 'fmtaLajGwyQ', 'cIiH15PhemI', 'm_39nFZZyNI', 'q5HNhva1Me8', 'JbCCy2DaJdk', 'Rtjqq-UtSqg', 'jrSDWX_qWwI', 'c4lDH3i9QFo', 'hiX1RNg9iiU', 'M4imfb3Flas', 'YbQ8itVSZWM', 'SWmRWdKnPf8', 'W2NfAjnxesU', 'aB1smFOEWVI', 'R49w4YjGPeg', '0sX-pIPUKFI', 'MXXVObSnx-I', 'NChLhqJiFck', '_pyyQZNz7j0', 'tYAlgEW_Nu8', 'bz9bLjFrfLE', 'aIDJRmk0ROM', 'vfC04Q0SABQ', 'Jt4ldjz5cDI', 'YzdWOnJcE60', 'JlkAp8Hw8-g', 'etsS26o8J1w', '6w_AqyZP49k', 'E40BilobTsk', 'xa9O6-i6rIQ', 'Gc4wHmyOf9E', 'CoEzDgpvAOo', 'g6TO9CJ_8mU', 'X4HMZp_1cys', '7zNGVg-wU2I', 'Z8fKSw2OVRg', 'lKfgy84G5D8', 'ILV1TzapHVE', 'jSiNiR5ePO0', 'XudUnEDXrpw', 'tO2xwpLxgLQ', 'obdm34QL6xg', '7I8OCYEWk_c', 't7qEMlLOS7Y', 'VjftAy7wS6g', '-Q6OmFiFtd4', 'IyK6lAMLjIA', 'DRHV9Qo_ufs', 'npkfzbGzn7g', 'Jfi4pQyYJkM', '4gLf3vg4KpE', 'hVao4M0pUDc', 'I5pKIVY8uS0', '2P6fHEGchQo', 'u9t7H_jI1Gc', 'D_k6iIu9y3g', 'jh9mfzLkJR8', '0kMSp8Deamk', '_JPWxRAOisQ', 'HqORH4vmdcQ', 'AGm8uzCXyBI', '1JN-QpwWDAQ', 'wZYelWzJcUE', 'WL1pSP5Z7u8', 'q55s11hp1sc', 'AWloXsb6qCE', 'OmIDh3wqQCk', 'rc8Rm0tfl4A', 'qvmWOVy6lKs', 'M016woop34c', 'UOX-pDThHm4', '_RDMphnpH4Y', 'k-z_5dGETTc', 'AeZD_rSXnfc', '5TbF5hauluQ', 'xBZKin0JXtc', 'TQPNiRZTi4Y', 'c0guXrqrHTw', 'GWRYWyURn4Y', 'ljUL8acNMZU', 'cGGmiQxNhOo', 'T7sQcm_tYt8', 'hsFwiFaSpXY', 'hrTpui-3el4']

    public_video_ids = filter_video_ids_to_public_videos_only(youtube, video_ids)
    add_to_stats_file(
        f'public_video_ids length: {len(public_video_ids)}',
        output_file_path
    )
    # public video ids length 292 on july 26th
    # public_video_ids = ['he2JBiIaSrw', 'B1td1aEja6Y', 'SV2j6uzP3pc', 'gb1kuBo57_Q', 'Gz3S_qf3Ub4', 'uFOksjM5QB8', '7LXH5nArL0o', 'zbbDL5wPfXI', 'Z82C8jPSIac', 'L9X-jvk3uMk', 'OHR9sBV_Odg', 'pxtuwaKnwLQ', '2RyUb03JxTM', '0VjpGPu4exQ', 'BtySKA5aIjU', 'AgM_meE8ncA', 'njq-sMdSNXs', '-GjNFBEpMl8', 'u2msyE_Xmts', 'oD0Y1UxEc2U', '2u61_W3Fg7o', '2ndBrRNVpzA', 'FO5OKw_enyg', 'HhDYYQK4p7c', 'MGGSQlPPc58', 'P12D2swA2NI', 'Sq_6AuPa_eE', 'ZP_ZjLN-RG8', 'aMrvhDXQ8b4', 'g4oWu11-7Ms', '_XnASY7ebRI', 'ShDU8sdb3OM', 'cU6_3dh9wx8', 'ESiAJ4VHsQI', '819T5hsQH-I', 'etL-7Nc6vM0', 'H4U79qWXF5Y', '3cTEt5HOHDM', 'GtNsLBLOB4M', 'SXuzwQm6wKI', 'SfjB7DawYcI', 'xdxrUG0oWPA', 'MppRhpD6Ga8', 'SfqWkh1XKw0', '2SQ5IVqxhqw', 'RYxaKMlZm20', 'roHyrenq0Kc', 'IGb5se9MJYk', 'jLL513Bwggs', 'yjMdGcF_ze8', 'sy-Shqj-tPE', 'jcPk1CfFS9w', '8MTuxM0SNDw', 'LNipM5a2KQU', '4dj01cSHIpo', 'F0OftsCKATA', 'a1XnaWrA-2U', 'R_4es5v8gT0', 'WiLn7Dk44Xs', 'ffIH5rOAK70', '_sIGf3YWUfA', 'YMNS8BvWJwM', 'DHx020oG5ig', 'Py-vHN0LJk8', 'budNrwsqNw8', '9hIOrV30n9o', 'o4pxpWt-v3g', 'jgGRqKt2nZk', '4v-lVyx0r2A', 'UHZgQXXkAnQ', '6VKtx1PyXh0', 'A7D04dl0Sy0', 'yMGa4uWFPO4', 'Kqp096g_vcI', 'IZZ7oT30VY4', 'tKrW_51FK1Q', 'Z1MtZKU9fRg', 'OXMZJT3Jf5M', 'GoGpqXcJYP0', 'Ub-z6LcW-iU', 'VccfBSzBoxg', 'FWLhYoK3xFE', '4fleXHCEtpI', 'R11VmoNCE2I', 'oYWbT1Fuz18', 'Vw04dXbBvqM', 'gReMDBLkwIk', '5HtrTsn8OkY', 'EgHksqIwlyQ', 'yzxG4OwAkqc', 'mnkSlUHu4RY', 'pkHlYQRnPUE', 'NVEnj8kAIwQ', 'ItOaJpfDq5w', 'j7Qo37PoOhM', 'GGZYKlIcS24', 'fGzLq6Ws0S8', 'G37aeuomwII', 'NrjL0tpOym4', 'SWffqpmsFW0', '1kPr1na1xtE', 'UBegb8Eg21Q', 'ysmuiTiJUo0', 'jfs0mubVz7A', 'Cj2Rl2c6bjo', '7iC-KH7NFbA', 'X1tpgkgy02M', 'IpC-WsRyINQ', 'YlL7rrEYlF0', 'jM6-txG11Os', 'cBBlsMBRJ-0', 'gQFF_HhOnKw', 'gLqig6DFj0s', 'mYkyWl9dCeI', 'XM1j7cAX9II', '_RtbiqUqqIk', 'B4-5wheRDwQ', 'UnXNbpfC4r8', '8YV4Q6cbguY', 'fwtJgewYgOo', 'rsJDW1nUl2s', 'Ple-MsFilOU', 'bTLQmnX1vmg', 'bkg8ch3GV90', 'K8vM6dfisuE', 'P4MSpd-ENog', '5ryf3SwNADI', 'oostn1TQ6t8', 'gpTnD6a3wqw', 'xwmkDg2JKy0', 'xJTvITUQ_is', 'bKINNP1b6zE', 'L9Lk08nKKVY', 'Ydx6DzrEp8w', 'wMCs2Py-Ldk', 'GApWG1N0tFc', 'UA3I3Rvj09w', 'Ms0CDpaDoIo', 'IfAElOseOiE', 'tWx9rLZDkrE', '7qcvJK1NyEM', 'j8QWfpLL02o', 'E_Lc7TCq4Ew', 'Wlmth0b8XkU', 'GZPguS75TFE', 'xvy8sNQ7dFE', 'YU_c22ZpTGM', 'fQNgVGy9eFc', 'GMFh9woyOv0', 'SHvzrcDs0pg', '6byaa1yQQk8', 'e8ZoWonhdOU', 'QKiXaXbU9wk', 'tbEtC0sgWi0', 'Iog5-hx9JYw', '2X2-tJmZ5Og', 'PzElD9BNuns', '-dIadOxzpqs', 'hnE-Ux_X_b8', 'QFhWS4qh2XY', 'ua7WHf-Kmek', 'R0J-MKjDnLg', 'KaW4NwIiBGk', 'HUdBeoKuC60', '4XVb8cFbRBs', 'hWhdGq6CGYM', 'HjlQWyvYNZM', '65LU1MNBCnA', 'snJ5Z5hU0uM', 'LZ9fx3uoZmc', 'MkhBRKnXVvY', 'VKzemMxXdXg', 'TKpsFGwCLj4', '46NAK_IgAJ0', 'iAAPu7l5sQA', '0HY0d_HZ2t8', 'OvIDo5OWyyE', 'vGuoOPOFHVM', '0-bWyvD6aks', 'KdjXaFSRGC8', 'lQoU6_uXa64', '5gmFZTu1vMM', 'TjJVUgM4iN0', 'fL6veYr1Em4', 'OwPoEj9YW8U', 'SapRuHCSj6k', 'VQ99g5jPNCE', 'L50omm2cbf0', 'Izkt_sc8-Io', 'fHPHVvrvpLk', 'Ypz05RTpeDg', 'BSXTkxHXF58', 'KAwmnGuZzWk', 'dRy8Y3hZE8c', 'Fpy1XR2Pcag', 'pELoBG9aZxY', 'plq8aD9o08g', 'IIThxk9tUa8', 'SQ9Bqre631w', 'UJJOlUg4a4A', 'vkOCX8WHTfg', 'xNMXbfJ5CLo', '8ly2yriqP7I', 'QQHjeSxitEw', 'm9KGXrOeUNA', 'e8t62Oz1fqs', 'e3n31VpF9dI', 'HoGOye_Rt50', 'e0h2NpiTsP0', 'Z2Peak8nkuY', 'odaPRfO2AGQ', 'fmtaLajGwyQ', 'cIiH15PhemI', 'm_39nFZZyNI', 'q5HNhva1Me8', 'JbCCy2DaJdk', 'Rtjqq-UtSqg', 'jrSDWX_qWwI', 'c4lDH3i9QFo', 'hiX1RNg9iiU', 'M4imfb3Flas', 'YbQ8itVSZWM', 'SWmRWdKnPf8', 'W2NfAjnxesU', 'aB1smFOEWVI', 'R49w4YjGPeg', '0sX-pIPUKFI', 'MXXVObSnx-I', 'NChLhqJiFck', '_pyyQZNz7j0', 'tYAlgEW_Nu8', 'bz9bLjFrfLE', 'aIDJRmk0ROM', 'vfC04Q0SABQ', 'Jt4ldjz5cDI', 'YzdWOnJcE60', 'JlkAp8Hw8-g', 'etsS26o8J1w', '6w_AqyZP49k', 'E40BilobTsk', 'xa9O6-i6rIQ', 'Gc4wHmyOf9E', 'CoEzDgpvAOo', 'X4HMZp_1cys', '7zNGVg-wU2I', 'Z8fKSw2OVRg', 'lKfgy84G5D8', 'ILV1TzapHVE', 'jSiNiR5ePO0', 'XudUnEDXrpw', 'tO2xwpLxgLQ', 'obdm34QL6xg', '7I8OCYEWk_c', 't7qEMlLOS7Y', 'VjftAy7wS6g', '-Q6OmFiFtd4', 'IyK6lAMLjIA', 'DRHV9Qo_ufs', 'npkfzbGzn7g', 'Jfi4pQyYJkM', '4gLf3vg4KpE', 'hVao4M0pUDc', 'I5pKIVY8uS0', '2P6fHEGchQo', 'u9t7H_jI1Gc', 'D_k6iIu9y3g', 'jh9mfzLkJR8', '0kMSp8Deamk', '_JPWxRAOisQ', 'HqORH4vmdcQ', 'AGm8uzCXyBI', '1JN-QpwWDAQ', 'wZYelWzJcUE', 'WL1pSP5Z7u8', 'q55s11hp1sc', 'AWloXsb6qCE', 'OmIDh3wqQCk', 'M016woop34c', 'UOX-pDThHm4', '_RDMphnpH4Y', 'k-z_5dGETTc', 'AeZD_rSXnfc', '5TbF5hauluQ', 'xBZKin0JXtc', 'TQPNiRZTi4Y', 'c0guXrqrHTw', 'GWRYWyURn4Y', 'ljUL8acNMZU', 'cGGmiQxNhOo', 'T7sQcm_tYt8', 'hsFwiFaSpXY', 'hrTpui-3el4']
    non_shorts_video_ids = filter_shorts_out_of_video_ids(youtube_analytics, public_video_ids)
    # non_shorts_video_ids = ['2u61_W3Fg7o', '2ndBrRNVpzA', '2SQ5IVqxhqw', 'RYxaKMlZm20', 'roHyrenq0Kc', 'IGb5se9MJYk', 'jLL513Bwggs', 'yjMdGcF_ze8', 'sy-Shqj-tPE', 'jcPk1CfFS9w', '8MTuxM0SNDw', 'LNipM5a2KQU', '4dj01cSHIpo', 'F0OftsCKATA', 'a1XnaWrA-2U', 'R_4es5v8gT0', 'WiLn7Dk44Xs', 'YMNS8BvWJwM', 'Py-vHN0LJk8', 'jgGRqKt2nZk', '6VKtx1PyXh0', 'Kqp096g_vcI', 'IZZ7oT30VY4', 'tKrW_51FK1Q', 'Z1MtZKU9fRg', 'OXMZJT3Jf5M', 'GoGpqXcJYP0', 'Ub-z6LcW-iU', 'VccfBSzBoxg', 'FWLhYoK3xFE', '4fleXHCEtpI', 'R11VmoNCE2I', 'oYWbT1Fuz18', 'Vw04dXbBvqM', 'gReMDBLkwIk', '5HtrTsn8OkY', 'yzxG4OwAkqc', 'j7Qo37PoOhM', 'GGZYKlIcS24', 'fGzLq6Ws0S8', 'G37aeuomwII', 'NrjL0tpOym4', 'SWffqpmsFW0', '1kPr1na1xtE', 'UBegb8Eg21Q', 'jfs0mubVz7A', 'Cj2Rl2c6bjo', '7iC-KH7NFbA', 'IpC-WsRyINQ', 'jM6-txG11Os', 'cBBlsMBRJ-0', 'gQFF_HhOnKw', 'gLqig6DFj0s', 'mYkyWl9dCeI', 'XM1j7cAX9II', '_RtbiqUqqIk', 'B4-5wheRDwQ', 'UnXNbpfC4r8', '8YV4Q6cbguY', 'fwtJgewYgOo', 'rsJDW1nUl2s', 'Ple-MsFilOU', 'bTLQmnX1vmg', 'bkg8ch3GV90', 'K8vM6dfisuE', 'P4MSpd-ENog', '5ryf3SwNADI', 'oostn1TQ6t8', 'gpTnD6a3wqw', 'xwmkDg2JKy0', 'xJTvITUQ_is', 'bKINNP1b6zE', 'L9Lk08nKKVY', 'Ydx6DzrEp8w', 'wMCs2Py-Ldk', 'tWx9rLZDkrE', '7qcvJK1NyEM', 'j8QWfpLL02o', 'E_Lc7TCq4Ew', 'Wlmth0b8XkU', 'GZPguS75TFE', 'fQNgVGy9eFc', 'GMFh9woyOv0', 'SHvzrcDs0pg', '6byaa1yQQk8', 'e8ZoWonhdOU', 'QKiXaXbU9wk', 'tbEtC0sgWi0', 'Iog5-hx9JYw', '2X2-tJmZ5Og', 'PzElD9BNuns', '-dIadOxzpqs', 'hnE-Ux_X_b8', 'QFhWS4qh2XY', 'ua7WHf-Kmek', 'R0J-MKjDnLg', 'KaW4NwIiBGk', 'HUdBeoKuC60', '4XVb8cFbRBs', 'hWhdGq6CGYM', 'HjlQWyvYNZM', '65LU1MNBCnA', 'snJ5Z5hU0uM', 'LZ9fx3uoZmc', 'MkhBRKnXVvY', 'VKzemMxXdXg', 'TKpsFGwCLj4', '46NAK_IgAJ0', 'iAAPu7l5sQA', '0HY0d_HZ2t8', 'OvIDo5OWyyE', 'vGuoOPOFHVM', '0-bWyvD6aks', 'KdjXaFSRGC8', 'lQoU6_uXa64', '5gmFZTu1vMM', 'TjJVUgM4iN0', 'fL6veYr1Em4', 'OwPoEj9YW8U', 'SapRuHCSj6k', 'VQ99g5jPNCE', 'L50omm2cbf0', 'Izkt_sc8-Io', 'fHPHVvrvpLk', 'Ypz05RTpeDg', 'BSXTkxHXF58', 'KAwmnGuZzWk', 'dRy8Y3hZE8c', 'Fpy1XR2Pcag', 'plq8aD9o08g', 'IIThxk9tUa8', 'UJJOlUg4a4A', 'vkOCX8WHTfg', '8ly2yriqP7I', 'm9KGXrOeUNA', 'e3n31VpF9dI', 'HoGOye_Rt50', 'cIiH15PhemI', 'q5HNhva1Me8', 'Rtjqq-UtSqg', 'jrSDWX_qWwI', 'c4lDH3i9QFo', 'hiX1RNg9iiU', 'M4imfb3Flas', 'YbQ8itVSZWM', 'SWmRWdKnPf8', 'W2NfAjnxesU', 'aB1smFOEWVI', 'R49w4YjGPeg', '0sX-pIPUKFI', 'MXXVObSnx-I', 'NChLhqJiFck', '_pyyQZNz7j0', 'tYAlgEW_Nu8', 'bz9bLjFrfLE', 'aIDJRmk0ROM', 'vfC04Q0SABQ', 'Jt4ldjz5cDI', 'YzdWOnJcE60', 'JlkAp8Hw8-g', 'etsS26o8J1w', '6w_AqyZP49k', 'E40BilobTsk', 'xa9O6-i6rIQ', 'Gc4wHmyOf9E', 'CoEzDgpvAOo', 'X4HMZp_1cys', '7zNGVg-wU2I', 'Z8fKSw2OVRg', 'lKfgy84G5D8', 'ILV1TzapHVE', 'jSiNiR5ePO0', 'XudUnEDXrpw', 'tO2xwpLxgLQ', 'obdm34QL6xg', '7I8OCYEWk_c', 't7qEMlLOS7Y', 'VjftAy7wS6g', '-Q6OmFiFtd4', 'IyK6lAMLjIA', 'DRHV9Qo_ufs', 'npkfzbGzn7g', 'Jfi4pQyYJkM', '4gLf3vg4KpE', 'hVao4M0pUDc', 'I5pKIVY8uS0', '2P6fHEGchQo', 'u9t7H_jI1Gc', 'D_k6iIu9y3g', 'jh9mfzLkJR8', '0kMSp8Deamk', '_JPWxRAOisQ', 'HqORH4vmdcQ', 'AGm8uzCXyBI', '1JN-QpwWDAQ', 'wZYelWzJcUE', 'WL1pSP5Z7u8', 'q55s11hp1sc', 'AWloXsb6qCE', 'OmIDh3wqQCk', 'M016woop34c', 'UOX-pDThHm4', '_RDMphnpH4Y', 'k-z_5dGETTc', 'AeZD_rSXnfc', '5TbF5hauluQ', 'xBZKin0JXtc', 'TQPNiRZTi4Y', 'c0guXrqrHTw', 'GWRYWyURn4Y', 'ljUL8acNMZU', 'cGGmiQxNhOo', 'T7sQcm_tYt8', 'hsFwiFaSpXY', 'hrTpui-3el4']
    add_to_stats_file(
        f'length of non_shorts_video_ids: {len(non_shorts_video_ids)}',
        output_file_path
    )

    # print(non_shorts_video_ids)
    watch_minutes = calculate_watch_time(youtube_analytics, non_shorts_video_ids,  start_date, end_date)
    print(watch_minutes)
    add_to_stats_file(
        f'watch_minutes: {watch_minutes}'
    )
    # print(video_ids)
    #pprint(response)



def add_to_stats_file(s, file_path):
    with open(file_path, 'a') as f:
        f.write(s + '\n')

def calculate_watch_time(youtube_analytics, non_shorts_video_ids, start_date, end_date):
    total_watch_minutes = 0
    for video_id in non_shorts_video_ids:
        response = execute_analytics_api_request(
            youtube_analytics.reports().query,
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            # dimensions="",
            # sort='day',
            metrics="estimatedMinutesWatched",
            filters=f'video=={video_id}'
        )
        total_watch_minutes += response['rows'][0][0]
        print(video_id, total_watch_minutes)
    return(total_watch_minutes)

def filter_shorts_out_of_video_ids(youtube_analytics, public_video_ids):
    non_shorts_video_ids = []
    for video_id in public_video_ids:
        response = execute_analytics_api_request(
            youtube_analytics.reports().query,
            ids='channel==MINE',
            startDate='2017-01-01',
            endDate='2023-12-31',
            dimensions="video,creatorContentType",
            # sort='day',
            metrics="views",
            filters=f'video=={video_id}'
        )
        if len(response['rows']) > 0:
            if response['rows'][0][1] == 'shorts':
                print(f'filter_shorts_out_of_video_ids: filtering out short, video_id: {video_id}')
                continue
            else:
                print(f'filter_shorts_out_of_video_ids: adding non-short video, video_id: {video_id}')
                non_shorts_video_ids.append(video_id)

        else:
            print(f'filter_shorts_out_of_video_ids: no information found for video_id: {video_id}')
    return non_shorts_video_ids


    return 'foo'

def get_youtube_for_analytics():
    API_SERVICE_NAME = 'youtubeAnalytics'
    API_VERSION = 'v2'
    CLIENT_SECRETS_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

    read_pickle = True
    write_pickle = False
    assert not (read_pickle and write_pickle)
    if read_pickle:
        with open('report_credentials.pickle', 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        if write_pickle:
            with open('report_credentials.pickle', 'wb') as f:
                pickle.dump(credentials, f)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def execute_analytics_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()

  return response


def do_test_thing(youtube_analytics):
    video_id = 'he2JBiIaSrw'
    try:
        response = execute_analytics_api_request(
            youtube_analytics.reports().query,
            ids='channel==MINE',
            startDate='2017-01-01',
            endDate='2023-12-31',
            dimensions="video,creatorContentType",
            # sort='day',
            metrics="views",
            filters='video==_sIGf3YWUfA'
        )
        # video GWRYWyURn4Y, videoOnDemand
        # video Z82C8jPSIac, no rows
    except HttpError as e:
        print('erroar', e)

    pprint(response)
    print('hello')

    request = youtube_analytics.videos().list(
        part="status,snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    privacy_status = response['items'][0]['status']['privacyStatus']
    if privacy_status == 'public':
        pass
        # add to list of public videos

    pprint(response)
    print('hello')


def filter_video_ids_to_public_videos_only(youtube, video_ids):
    public_video_ids = []
    for video_id in video_ids:
        request = youtube.videos().list(
            part="status,snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        privacy_status = response['items'][0]['status']['privacyStatus']
        if privacy_status == 'public':
            public_video_ids.append(video_id)
    return public_video_ids


def get_all_video_ids_for_my_channel(youtube) -> [str]:

    search = youtube.search()
    request = search.list(
        part="snippet",
        forMine=True,
        maxResults=25,
        type="video"
    )
    search_docs = []
    while request is not None:
        search_doc = request.execute()
        search_docs.append(search_doc)
        request = search.list_next(request, search_doc)
    # print(search_docs)
    video_ids = []
    for search_doc in search_docs:
        for item in search_doc['items']:
            video_ids.append(item['id']['videoId'])

    return video_ids


    #activities = service.activities()
    #request = activities.list(userId='someUserId', collection='public')

    #while request is not None:
        #activities_doc = request.execute()

        # Do something with the activities

        # request = activities.list_next(request, activities_doc)



    # responses = []
    # request = youtube.search().list(
    #     part="snippet",
    #     forMine=True,
    #     maxResults=25,
    #     type="video"
    # )
    # response = request.execute()
    # responses.append(response)
    # while response.get('nextPageToken') is not None:
    #     request = youtube.search().list(
    #         part="snippet",
    #         forMine=True,
    #         maxResults=25,
    #         type="video",
    #         params=f'nextPageToken:{response.get("nextPageToken")}'
    #     )
    #     response = request.execute()
    #     responses.append(response)

    # print('hello')
    #
    # video_ids = []
    # for item in response['items']:
    #     video_ids.append(item["id"]["videoId"])
    # return video_ids
    # pprint(response)

def get_youtube():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    read_pickle = True
    write_pickle = False
    assert not (read_pickle and write_pickle)
    if read_pickle:
        with open('credentials.pickle', 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
    if write_pickle:
        with open('credentials.pickle', 'wb') as f:
            pickle.dump(credentials, f)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube




if __name__ == "__main__":
    main()

