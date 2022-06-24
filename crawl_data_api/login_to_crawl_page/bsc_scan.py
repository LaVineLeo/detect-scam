import requests

cookies = {
    '__stripe_mid': '0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74',
    'bscscan_cookieconsent': 'True',
    'cf_clearance': 'xfkOOpWdrtVi.JpRFTm5cMZZLN3k6xZkdP14MgdJWR0-1655279288-0-150',
    '__cuid': '49772a01dd2442d897ca9efb95c0679e',
    'amp_fef1e8': 'e28591fc-3928-47d5-80ba-92c06d3887acR...1g6035vs6.1g6035vsa.17.5.1c',
    'ASP.NET_SessionId': 's4qaeudrzrrmti0ffslsy1vz',
    '__cflb': '02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njFTxtwBvf38Hek',
    '_gid': 'GA1.2.788481277.1656060614',
    '_gat_gtag_UA_46998878_23': '1',
    '__cf_bm': 'EfhJuVGo3mBaIr5KPLFphYBzhwvOIieRBmaoMgGrR0A-1656060620-0-AYGFvHarGeFFuySOdXc1YIt1EmRKZ4iId6ub5rJI923OtH7I4NXwsF2x6+Ve33ePL5WUWVRjQCimc7lYAtsMiQqbiVzo7BtatB5gM0aKii1hIF5GK0359Ux5S3iXMidpQQ==',
    '_ga_PQY6J2Q8EP': 'GS1.1.1656060613.30.1.1656060627.0',
    '_ga': 'GA1.2.608546645.1654740748',
    '__stripe_sid': '36ff570d-7b60-4ab3-81b5-c948a9bf498f5a1021',
}

headers = {
    'authority': 'bscscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '__stripe_mid=0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74; bscscan_cookieconsent=True; cf_clearance=xfkOOpWdrtVi.JpRFTm5cMZZLN3k6xZkdP14MgdJWR0-1655279288-0-150; __cuid=49772a01dd2442d897ca9efb95c0679e; amp_fef1e8=e28591fc-3928-47d5-80ba-92c06d3887acR...1g6035vs6.1g6035vsa.17.5.1c; ASP.NET_SessionId=s4qaeudrzrrmti0ffslsy1vz; __cflb=02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njFTxtwBvf38Hek; _gid=GA1.2.788481277.1656060614; _gat_gtag_UA_46998878_23=1; __cf_bm=EfhJuVGo3mBaIr5KPLFphYBzhwvOIieRBmaoMgGrR0A-1656060620-0-AYGFvHarGeFFuySOdXc1YIt1EmRKZ4iId6ub5rJI923OtH7I4NXwsF2x6+Ve33ePL5WUWVRjQCimc7lYAtsMiQqbiVzo7BtatB5gM0aKii1hIF5GK0359Ux5S3iXMidpQQ==; _ga_PQY6J2Q8EP=GS1.1.1656060613.30.1.1656060627.0; _ga=GA1.2.608546645.1654740748; __stripe_sid=36ff570d-7b60-4ab3-81b5-c948a9bf498f5a1021',
    'origin': 'https://bscscan.com',
    'referer': 'https://bscscan.com/login',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
}

data = {
    '__VIEWSTATE': '27aXpeXSuZ07Cz/yEFx4Wn/fmzF6243lh+irNoOlQZz53r+0ujVYsl/RPIlaJovBwV7CEGwgqJE4X0jAufsOthse/39pQhq2ltXpCZoRYssXd2rWESaOzdkxYVFE84hIzxG+cr3RnWfr6HaLDsUKRQtvklZcNdXsAU2UWT8R5HVQqvssfBEqVzl1KUnkfxM5QFTaC70WMcYNk3yNENssVq/LK6Xt8MTm3YDGXEU2Uu2KkFOly1aFOZcTKIOl2OIQo5oaty1yWGxQdpO1x4RYb2OfEFThNcdPlr4sBWANSYR+mVj4nnWCBJiTpqx6T6WYQq6rdq8XnGqYzD78mG04owlNYl+RFQpFz/9wpn2S0xU0eyzzlKKihTPvAp53CgCn178mb1poUOI6jyAaMSKjril1wHaS0A/LcoeGxoeosOjKMDqDpufM3EXjskVYqG80bWo9xnYa9LEy2Uc+lGa4COQq+ST0BnZEQ4mkzEXaBYuUZPaUZBuVVfNw+/xWLwWn8iAfvzZqkj4x9A2rlYAGJ4z34Fhei0b0vUS94/Xz9gClcFfuobf9i1DNivZnojTQkUEZxxU+uvdoU2Oo0n2ng7BCYJJOoaloTF0ZcpCIYCLESfy4G8lMAQEa36F52WDZ/hTXg3MNyULZf2/SFLauFNGS5UrCzbK+ep0DN3fCl15gOzoSIsi/9c26XhfQDatjX5DxnmlTNmPQ0A2kJ52MYja5jyJ+UEZGoq7ivaehuRsUhz1WeWleuwPyxWUNlAxz1jCHRg7V1ZYQpqHjroI5oAxY34ihca0CukcXgnE5kF0aqttUIi8WDh4hYrTnfRJOtyXU2HthXQhYknaitXgU5I+9LDDepoOb3qDn6qdzIUuXsrJGI/LULMrrb6GBYrPxTO0Py+RCkqK0Ta4YVWvE0+e7NsKmckirOaDQhRi6G64QdSbZM5O2zJ9IHvdTQgWmgGN3jlUw0OEEOKUXe69nPNCxTRyTXz2D2vtk3US1GPAS7WphGbX2sn+GHUMccVqkNJVo1TjiFKn5sX/TMndLtPXOgOcLCKdphQdGkFqJI0xdoZPs9xj6aZ/1NdTWnLjk+savNSefB/iHngz17VAxn9DQ4LYR7B4pYqMthhvMztDyHpWjgIAvoT6Gbyezx7s2B5NtuDlwqcQyNzrVtAGjfV+li3g7mOB0zzwirVvAfr5eErxNvn5dC2hM5pLKRKIMRWGL9fDuxio5fUyaP+qs0gIkGsmHvpUrTvWEDnSQPT2BPxXJ/quGoaYWYs1xRg5AyQSCLp64+6r3thUyl5LUnWTW0IR/1kd/LFw1WOsBCiBk1hts1lQ5RKRmBh1iQosOmE0uWEziAs18D+Dpkh+e8g==',
    '__VIEWSTATEGENERATOR': 'C2EE9ABB',
    '__EVENTVALIDATION': 'jHnYWNfTGRxXsriqqizLHoU88bZeRRT9gGh6not9NmCEbAIoJ7ZOMU5y19IVSlYN0nfH0b0bQMeuSEM4kyk4D7dCZuomwO2HPP3KgtuvYd8CsmibdN+ZUlZlCPgw7qRs1j5QrCGYQSafSy6VnMZCDLLCULL39aeAAQdvzbI/fLO4bJmK09t0rfGA4wBXbK3Z',
    'ctl00$ContentPlaceHolder1$txtUserName': 'truongtnn404',
    'ctl00$ContentPlaceHolder1$txtPassword': 'lhhuong80045',
    'g-recaptcha-response': '',
    'ctl00$ContentPlaceHolder1$btnLogin': 'LOGIN',
}

response = requests.post('https://bscscan.com/login', cookies=cookies, headers=headers, data=data)