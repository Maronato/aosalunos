CRAWLERS_NAMES = {
    'bing': 'Bingbot',
    'google': 'Googlebot',
    'yahoo': 'Yahoo! Slurp',
    'yahooch': 'Yahoo! Slurp China',
    'unidentified': 'Unidentified',
}

CRAWLERS_AGENTS = {
    'bingbot/': 'bing',
    'Googlebot/': 'google',
    'Yahoo! Slurp China': 'yahooch',
    'Yahoo! Slurp': 'yahoo',
    'bot': 'unidentified',
    'Bot': 'unidentified',
    'BOT': 'unidentified',
}

CRAWLERS_HOSTS = {
}


class Crawler(object):
    crawler = False
    host = None
    username = None

    def __init__(self, agent = None, ip = None):
        if agent is not None:
            for item in CRAWLERS_AGENTS.keys():
            	if agent.find(item) != -1:
                    self.crawler = True
                    self.username = CRAWLERS_AGENTS[item]
                    break

        if ip is not None:
            for item in CRAWLERS_HOSTS.keys():
            	if ip == item:
                    self.crawler = True
                    self.username = CRAWLERS_HOSTS[item]
                    break

        if self.crawler:
            self.username = CRAWLERS_NAMES[self.username]
            self.host = ip