

# Personal 8a Link
my8aURL = "https://www.8a.nu/scorecard/david-vasko/boulders/?AscentClass=0&AscentListViewType=0&GID=d96e250ee9136da4105514a70e6e38e8"

# List of dictionarys United Statesed in transforming 8a specific strings.
# > These are highly likely to change in the future and will
# > need to be redefined
currentGradeMap = {
    "A8_8a2f2ba201c69c72f5fae6d5b490ca31()": "15",
    "A8_371ada172e6aca6d36030cff991c2110()": "14",
    "A8_70ae3987db297649adfa22ec835bbef5()": "13",
    "A8_f94c1a7c1ade88cfeb2bd73ffa116d9f()": "12",
    "A8_59b85d692c593f314ed49d15870ff8d2()": "11",
    "A8_ea3a0c3e0e84736e61d7b4ae4aa07145()": "10",
    "A8_2d8a2dca8da8f8595bfafa25580f88c4()": "9",
    "A8_ebe1c7b6a0324f26fa1203e423827d73()": "8",
    "A8_a3ef9ab41d342fca7c6d3bf3b2e01ca2()": "7/8",
    "A8_b68c76e55910e67faca8829b4700d2e1()": "7",
    "A8_728a1685254b76fb0532dd2bd83fc670()": "6",
    "A8_323b60c5b47a45c73f666867fd27b319()": "5/6",
    "A8_59ed716391fbf46727ad091b93b1b507()": "5",
    "A8_8e761f5120d8a81b268c721eb940f633()": "4/5",
    "A8_4b0680d2e6545260c512c8424e7d0180()": "4",
    "A8_31d055ac30224e9cb434b74b6f77c9fe()": "3/4",
    "A8_3cd6d35aa8f427f02d106c1c40969227()": "3",
    "A8_b69a020c915c748aba94ed6c86226541()": "2",
    "A8_10d988d607dfa42c867b638336965a99()": "1",
    "A8_217b0d256645bca88490d2f8257ffecd()": "0",
    "A8_027540acd8eb24681172603ebf359a5c()": "B",
    "A8_5e6e11644ad74bc7fa3554dc12d16d5d()": "B",
    "A8_d02544d610dbfd7bb34cb85ff612365c()": "B"

}
currentAscentTypeMap = {
    "/scorecard/images/56f871c6548ae32aaa78672c1996df7f.gif": "flash",
    "/scorecard/images/979607b133a6622a1fc3443e564d9577.gif": "redpoint",
    "/scorecard/images/e37046f07ac72e84f91d7f29f8455b58.gif": "onsite"
}
recommendMap = {
    "/scorecard/images/UserRecommended_1.gif": True,
    "/scorecard/images/UserRecommended_0.gif": False
}

# Headers from inspecting te desired request on 8a.nu directly
headers = {
    "Host": "www.8a.nu",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Sec-Fetch-Site": "same-origin",
    "Referer": "https://www.8a.nu/user/My8a.aspx",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}

# 8a Specific Scraping Variables (high chance of changing)
ascentStartMarker = "<!-- Ascents -->"
ascentEndMarker = "</table>"

# Known Equivalences
areaEquivalences = {
    "MOUNT_WOODSON": "MT_WOODSON",
    "THE_BRICKYARD": "BRICKYARD"
}

# Manually maintained dictionary to get "country" + State
areaMaps = {
    "MINERAL_KING": {"country": "United States", "div1": "CA", "div2": "Sequoia"},
    "RANCHO_PENASQUITOS_CANYON": {"country": "United States", "div1": "CA", "div2": "San Diego"},
    "MT_WOODSON": {"country": "United States", "div1": "CA", "div2": "San Diego"},
    "SUPER_SLAB": {"country": "United States", "div1": "CA", "div2": "Sonoma"},
    "SALT_POINT": {"country": "United States", "div1": "CA", "div2": "Sonoma"},
    "MOUNT_BALDY": {"country": "United States", "div1": "CA", "div2": "Los Angeles"},
    "POMO_CANYON": {"country": "United States", "div1": "CA", "div2": "Sonoma"},
    "TRAMWAY": {"country": "United States", "div1": "CA", "div2": "San Jacinto"},
    "BISHOP": {"country": "United States", "div1": "CA", "div2": "Bishop"},
    "BLACK_MOUNTAIN": {"country": "United States", "div1": "CA", "div2": "San Jacinto"},
    "MARION_MOUNTAIN": {"country": "United States", "div1": "CA", "div2": "San Jacinto"},
    "TUOLUMNE_MEADOWS": {"country": "United States", "div1": "CA", "div2": "Yosemite"},
    "BRICKYARD": {"country": "United States", "div1": "CA", "div2": "Santa Barbara"},
    "JOSHUA_TREE": {"country": "United States", "div1": "CA", "div2": "Joshua Tree"},
    "YOSEMITE": {"country": "United States", "div1": "CA", "div2": "Yosemite"},
    "MT_TAMALPAIS": {"country": "United States", "div1": "CA", "div2": "San Fransisco"},
    "JUPITER_BOULDERS": {"country": "United States", "div1": "CA", "div2": "San Jacinto"},
    "MALIBU_TUNNEL_BOULDERS": {"country": "United States", "div1": "CA", "div2": "Los Angeles"},
    "DOOMSDAY_BOULDERS": {"country": "United States", "div1": "CA", "div2": ""},
    "TEMPORAL_BOULDERS": {"country": "United States", "div1": "CA", "div2": "Los Angeles"},
    "CAZADERO": {"country": "United States", "div1": "CA", "div2": "Sonoma"},
    "THE_DEPOT": {"country": "United States", "div1": "OR", "div2": "Bend"},
    "TELLURIDE": {"country": "United States", "div1": "CO", "div2": "Telluride"},
    "WALKER_RANCH": {"country": "United States", "div1": "CO", "div2": "Boulder"},
    "KLETTERGARDEN": {"country": "United States", "div1": "CO", "div2": "Denver"},
    "BARN_CANYON": {"country": "United States", "div1": "NM", "div2": "Gallup"},
    "WAIMEA_BAY_HI": {"country": "United States", "div1": "HI", "div2": "Waimea Bay"},
    "JOES_VALLEY": {"country": "United States", "div1": "UT", "div2": "Orangeville"},
    "LEAVENWORTH": {"country": "United States", "div1": "WA", "div2": "Leavenworth"},
    "SASQUATCH": {"country": "United States", "div1": "WA", "div2": "Seattle"},
    "SERVICE_BOULDER": {"country": "United States", "div1": "AK", "div2": "Anchorage"},
    "ISLE_OF_SKYE": {"country": "United Kingdom", "div1": "Scotland", "div2": "Isle of Skye"},
    "KHAJAGUDA": {"country": "India", "div1": "Telangana", "div2": "Khajaguda"}
}
stateEquivalences = {
    "CA": "California",
    "OR": "Oregon",
    "AK": "Alaska",
    "WA": "Washington",
    "NM": "New Mexico",
    "HI": "Hawaii",
    "UT": "Utah"
}
