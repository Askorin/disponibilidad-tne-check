import requests
from bs4 import BeautifulSoup

def estado_checker(url: str, url_rut: str, headers: dict[str, str]):
    with requests.Session() as s:
        r = s.get(url, headers = headers)
        r = s.get(url_rut, headers = headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        datos = str(soup.findAll('script')[1])

    for ch in ['\n', '\t', '<script>', '</script>']:
        datos.replace(ch, '')

    datos = datos.split(sep = ';')
    needle = 'parent.document.frm_tne.tne_estado_tne.value'

    for elem in datos:
        if elem.find(needle) >= 0:
            estado = elem.split(sep = '=')[1]
            break
    for i, char in enumerate(estado):
        if char == "'":
            break
        else:
            estado = estado[i+1:]
    for i, char in enumerate(estado):
        if char == '':
            estado = estado[0:i]

    estado = estado.replace("'", '')
    return estado

def send_teams(webhook_url: str, content: str, title: str, color: str):
    response = requests.post(
        url = webhook_url,
        headers ={"Content-Type": "application/json"},
        json = {
            "themeColor": color,
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": content
            }],
        },
    )
    return response.status_code

def main():
    # Browser user agent
    user_agent = '' 
    # De tal manera rut es: 123456789-0 
    rut_pre, rut_dig_verificador = '123456789', '0'

    headers = {
        'User-Agent': f'{user_agent}'
    }

    url = 'https://sistema.tne.cl/reposiciones/estado_tarjeta_alumno'
    url_rut = f'https://sistema.tne.cl/reposiciones/estado_tarjeta_alumno/tneEmitidas/{rut_pre}/{rut_dig_verificador}/'

    title = "Notificación Automatizada Estado TNE"
    content = f"<br>{estado_checker(url, url_rut, headers)}<br>"
    # Esto ocupa un webhook por teams
    teams_url = ''
    send_teams(teams_url, content, title, '00FF00')


if __name__ == '__main__':
    main()
