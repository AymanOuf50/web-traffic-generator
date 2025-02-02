from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import random
import time

# Liste des proxies (échantillon unique pour éviter les doublons)
proxies_list = [
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"},
  {"http": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001", "https": "http://proweb-zone-resi-region-fr:proweb123@b22b45d55a6e3328.yiu.us.ip2world.vip:6001"}

]

# Configuration de Selenium et de ChromeDriver
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")

    # Ajouter un proxy aléatoire
    proxy = get_random_proxy()
    chrome_options.add_argument(f"--proxy-server={proxy}")

    service = Service(r"C:\\Users\\hp\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)

# Sélectionner un proxy aléatoire
def get_random_proxy():
    if not proxies_list:
        raise Exception("Aucun proxy disponible.")
    return random.choice(proxies_list)

# Configuration par défaut
class ConfigClass:
    MAX_DEPTH = 5  # Niveau maximum de profondeur
    MIN_DEPTH = 3  # Niveau minimum de profondeur
    MAX_WAIT = 30  # Temps max entre les requêtes (en secondes)
    MIN_WAIT = 5  # Temps min entre les requêtes (en secondes)
    DEBUG = True  # Activer/désactiver les messages de débogage
    ROOT_URLS = [
        "https://www.rackoccasion.fr/",
        "https://rachat-rack-occasion.fr/"
    ]
    BLACKLIST = [
        'facebook.com',
        'pinterest.com'
    ]

config = ConfigClass()

# Couleurs pour les messages de débogage
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    NONE = '\033[0m'

# Affichage des messages de débogage
def debug_print(message, color=Colors.NONE):
    if config.DEBUG:
        print(f"{color}[DEBUG] {message}{Colors.NONE}")

# Récupérer tous les liens valides d'une page web
def get_links(driver):
    links = []
    elements = driver.find_elements(By.TAG_NAME, "a")
    for element in elements:
        try:
            link = element.get_attribute("href")
            if link and link.startswith("http") and not any(blacklisted in link for blacklisted in config.BLACKLIST):
                links.append(link)
        except Exception as e:
            debug_print(f"Erreur lors de la récupération des liens : {e}", Colors.RED)
    return links

# Parcours récursif d'une URL
def recursive_browse(driver, url, depth):
    debug_print(f"Navigation : {url} (profondeur restante : {depth})")
    if depth <= 0:
        return

    try:
        driver.get(url)  # Charger l'URL
        time.sleep(random.uniform(config.MIN_WAIT, config.MAX_WAIT))  # Attendre le chargement

        links = get_links(driver)
        if not links:
            debug_print(f"Aucun lien valide trouvé sur {url}", Colors.YELLOW)
            return

        next_url = random.choice(links)  # Sélectionner un lien aléatoire
        recursive_browse(driver, next_url, depth - 1)
    except Exception as e:
        debug_print(f"Erreur dans recursive_browse : {e}", Colors.RED)

# Point d'entrée principal
def main():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Générateur de trafic (Selenium)")
    print(f"Exploration entre {config.MIN_DEPTH} et {config.MAX_DEPTH} niveaux de profondeur")
    print(f"Temps d'attente entre {config.MIN_WAIT} et {config.MAX_WAIT} secondes")
    print("Appuyez sur Ctrl+C pour arrêter.")

    driver = get_driver()
    try:
        while True:
            random_url = random.choice(config.ROOT_URLS)
            depth = random.randint(config.MIN_DEPTH, config.MAX_DEPTH)
            recursive_browse(driver, random_url, depth)
    except KeyboardInterrupt:
        print("\nArrêt du générateur de trafic.")
    except Exception as e:
        debug_print(f"Erreur principale : {e}", Colors.RED)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
