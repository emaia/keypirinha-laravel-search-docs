# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

import json

APP = 'BH4D9OD16A'
KEY = '7dc4fe97e150304d1bf34f5043f178c4'
INDEX = 'laravel'

headers = {
    'X-Algolia-Application-Id': APP,
    'X-Algolia-API-Key': KEY,
    'Content-Type': 'application/json; charset=UTF-8'
}

url = 'https://'+APP+'-dsn.algolia.net/1/indexes/'+INDEX+'/query'

class laravel(kp.Plugin):
    """
    Search and open Laravel documentation.

    """
    def __init__(self):
        super().__init__()

    def on_start(self):
        pass

    def on_catalog(self):
        self.set_catalog([
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Laravel Docs (Master)",
                short_desc="Search through official Laravel documentation (master)",
                target="master",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.KEEPALL
            ),
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Laravel Docs (8.x)",
                short_desc="Search through official Laravel documentation (v8.x)",
                target="8.x",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.KEEPALL
            ),
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Laravel Docs (6.x)",
                short_desc="Search through official Laravel documentation (v6.x)",
                target="6.x",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.KEEPALL
            )
        ])

    def on_suggest(self, user_input, items_chain):

        suggestions = []

        if not items_chain or items_chain[0].category() != kp.ItemCategory.KEYWORD:
            return

        if len(user_input) > 0 and self.should_terminate(0.300):
            return

        payload = { 'params': 'query='+user_input+'&facetFilters=version:'+items_chain[0].target() }

        opener = kpnet.build_urllib_opener()
        opener.addheaders = [("X-Algolia-Application-Id", APP),("X-Algolia-API-Key", KEY),("Content-Type", "application/json; charset=UTF-8")]

        with opener.open(url, data=json.dumps(payload).encode()) as response:
            data = json.loads(response.read().decode("utf-8"))

        for hit in (data["hits"]):
            suggestions.append(
                self.create_item(
                    category=kp.ItemCategory.USER_BASE + 2,
                    label=hit['hierarchy']['lvl0'],
                    short_desc=hit['hierarchy']['lvl0'] + " » " + hit['hierarchy']['lvl1'] + " » " + hit['hierarchy']['lvl2'],
                    target=hit['url'],
                    data_bag=hit['url'],
                    args_hint=kp.ItemArgsHint.FORBIDDEN,
                    hit_hint=kp.ItemHitHint.IGNORE,
                )
            )

        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        kpu.web_browser_command(private_mode=None, new_window=None, url=item.data_bag(), execute=True)
        return

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass
