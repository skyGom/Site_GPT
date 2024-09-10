from urllib.parse import urlparse, urlunparse

def ensure_sitemap_url(url):
    parsed_url = urlparse(url)
    
    if not parsed_url.path.endswith('/sitemap-0.xml'):
        if parsed_url.path == '' or parsed_url.path.endswith('/'):
            new_path = parsed_url.path + 'sitemap-0.xml'
        else:
            new_path = parsed_url.path + '/sitemap-0.xml'

        updated_url = parsed_url._replace(path=new_path)
        return urlunparse(updated_url)
    
    return url

def extract_site_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc