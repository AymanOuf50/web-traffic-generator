import requests
import re
import time
import random

# Configuration par défaut
class ConfigClass:
    MAX_DEPTH = 10  # Niveau maximum de profondeur
    MIN_DEPTH = 3   # Niveau minimum de profondeur
    MAX_WAIT = 30   # Temps max entre les requêtes (en secondes)
    MIN_WAIT = 5    # Temps min entre les requêtes (en secondes)
    DEBUG = True    # Activer/désactiver les messages de débogage
    ROOT_URLS = [
        "https://safqat.proweb.ma"
    ]
    BLACKLIST = [
        'facebook.com',
        'pinterest.com'
    ]
    USER_AGENT = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/56.0.2924.87 Safari/537.36'
    )

config = ConfigClass()

# Liste des proxies
proxies_list = [
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"},
    {"http": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001", "https": "http://testsimokaid-zone-resi-region-fr:testsimokaid@e3a54aa59779d563.nbd.us.ip2world.vip:6001"}
]
    


class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    NONE = '\033[0m'

def debug_print(message, color=Colors.NONE):
    """Affiche des messages de débogage si activé."""
    if config.DEBUG:
        print(f"{color}[DEBUG] {message}{Colors.NONE}")

def get_random_proxy():
    """Sélectionne un proxy valide depuis la liste."""
    while proxies_list:
        proxy = random.choice(proxies_list)
        try:
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxy,
                timeout=5
            )
            print(f"Proxy valide : {proxy} | Réponse : {response.json()}")
            return proxy
        except requests.exceptions.RequestException:
            print(f"Proxy invalide : {proxy}. Suppression de la liste.")
            proxies_list.remove(proxy)
    raise Exception("Aucun proxy valide disponible.")

def do_request(url):
    """Effectue une requête HTTP en utilisant un proxy."""
    headers = {'User-Agent': config.USER_AGENT}
    try:
        proxy = get_random_proxy()
        response = requests.get(
            url,
            headers=headers,
            proxies=proxy,
            timeout=5
        )
        return response
    except Exception as e:
        debug_print(f"Échec de la requête. Erreur : {e}", Colors.RED)
        return None

def get_links(page):
    """Récupère tous les liens valides d'une page web."""
    pattern = r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
    links = re.findall(pattern, page.content.decode('utf-8', 'ignore'))
    return [
        link for link in links
        if not any(blacklisted in link for blacklisted in config.BLACKLIST)
    ]

def recursive_browse(url, depth):
    """Parcours récursif d'une URL."""
    debug_print(f"Navigation récursive : {url} (profondeur : {depth})")
    if depth <= 0:
        return

    try:
        page = do_request(url)
        if not page:
            debug_print(f"Échec lors de l'accès à {url}", Colors.YELLOW)
            return

        links = get_links(page)
        if not links:
            debug_print(f"Aucun lien valide trouvé sur {url}", Colors.YELLOW)
            return

        next_url = random.choice(links)
        time.sleep(random.uniform(config.MIN_WAIT, config.MAX_WAIT))
        recursive_browse(next_url, depth - 1)
    except Exception as e:
        debug_print(f"Erreur dans recursive_browse : {e}", Colors.RED)

def main():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Générateur de trafic démarré")
    print(f"Exploration entre {config.MIN_DEPTH} et {config.MAX_DEPTH} liens de profondeur")
    print(f"En attente entre {config.MIN_WAIT} et {config.MAX_WAIT} secondes entre les requêtes")
    print("Appuyez sur Ctrl+C pour arrêter.")

    while True:
        random_url = random.choice(config.ROOT_URLS)
        depth = random.randint(config.MIN_DEPTH, config.MAX_DEPTH)
        try:
            recursive_browse(random_url, depth)
        except Exception as e:
            print(f"Erreur : {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt du générateur de trafic.")
