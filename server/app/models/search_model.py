import asyncio
from scrapers.amazon.amazon_spyder import AmazonSpyder
from scrapers.olx.olx_spyder import OLX_Spyder
from scrapers.badr.badr_spyder import BadrSpyder
from scrapers.sigma.sigma_spyder import SigmaSpyder
from scrapers.alfrensia.alfrensia_spyder import ALFrensia_Spyder

class SearchModel:
    async def async_search_products(self, search_term, source_filters):
        results = {
            'olx': [],
            'sigma': [],
            'amazon': [],
            'badr': [],
            'alfrensia': []
        }

        tasks = []

        if source_filters.get('amazon'):
            amazon_spyder = AmazonSpyder()
            tasks.append(amazon_spyder.search_products_async(search_term))

        if source_filters.get('olx'):
            olx_spyder = OLX_Spyder(search_term)
            tasks.append(olx_spyder.scrape())

        if source_filters.get('badr'):
            badr_spyder = BadrSpyder()
            tasks.append(badr_spyder.scrap(search_term))

        if source_filters.get('sigma'):
            sigma_spyder = SigmaSpyder(search_term)
            tasks.append(sigma_spyder.scrape())

        if source_filters.get('alfrensia'):
            alfrensia_spyder = ALFrensia_Spyder()
            tasks.append(alfrensia_spyder.scrap(search_term))

        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        if source_filters.get('amazon'):
            if isinstance(results_list[0], Exception):
                results['amazon'] = [f"Error scraping Amazon: {str(results_list[0])}"]
            else:
                results['amazon'] = results_list[0] or []

        if source_filters.get('olx'):
            if isinstance(results_list[1], Exception):
                results['olx'] = [f"Error scraping OLX: {str(results_list[1])}"]
            else:
                results['olx'] = results_list[1] or []

        if source_filters.get('badr'):
            if isinstance(results_list[2], Exception):
                results['badr'] = [f"Error scraping Badr: {str(results_list[2])}"]
            else:
                results['badr'] = results_list[2] or []

        if source_filters.get('sigma'):
            if isinstance(results_list[3], Exception):
                results['sigma'] = [f"Error scraping Sigma: {str(results_list[3])}"]
            else:
                results['sigma'] = results_list[3] or []

        if source_filters.get('alfrensia'):
            if isinstance(results_list[4], Exception):
                results['alfrensia'] = [f"Error scraping ALFrensia: {str(results_list[4])}"]
            else:
                results['alfrensia'] = results_list[4] or []

        return results