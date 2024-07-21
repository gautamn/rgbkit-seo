
def find_missing_urls(all_live_urls_path, new_urls_path) -> None:
    # Read URLs from the files
    with open(all_live_urls_path, "r") as f:
        all_live_urls = set(line.strip() for line in f)

    with open(new_urls_path, "r") as f:
       new_urls = set(line.strip() for line in f)

    # Find URLs that are in all-liveurls-19072024.txt but not in new_urls.txt
    unique_urls = all_live_urls - new_urls

    # Print or save the unique URLs
    for url in unique_urls:
        print(url)
