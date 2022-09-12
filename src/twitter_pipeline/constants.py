TWEET_FIELDS = ["attachments", "author_id", "context_annotations", "conversation_id", "created_at", "entities", "geo",
                "id", "in_reply_to_user_id", "lang", "possibly_sensitive", "public_metrics", "referenced_tweets",
                "reply_settings", "source", "text", "withheld"]

EXPANSIONS = ["attachments.media_keys", "attachments.poll_ids", "author_id", "entities.mentions.username",
              "geo.place_id", "in_reply_to_user_id", "referenced_tweets.id", "referenced_tweets.id.author_id"]

MEDIA_FIELDS = ["alt_text", "duration_ms", "height", "media_key", "preview_image_url", "public_metrics", "type,url",
                "variants", "width"]

POLL_FIELDS = ["duration_minutes", "end_datetime", "id", "options", "voting_status"]

USER_FIELDS = ["created_at", "description", "entities", "id", "location", "name", "pinned_tweet_id",
               "profile_image_url", "protected", "public_metrics", "url", "username", "verified", "withheld"]

PLACE_FIELDS = ["contained_within", "country", "country_code", "full_name", "geo", "id", "name", "place_type"]

EN_MYTH_TWITTER_ID = [
    1283653858510598144,  # mori calliope
    1283646922406760448,  # takanashi kiara
    1283650008835743744,  # ninomae inanis
    1283657064410017793,  # gawr gura
    1283656034305769472  # watson amelia
]

EN_VSINGER_TWITTER_ID = [1363705980261855232]  # IRyS

EN_COUNCIL_TWITTER_ID = [
    1409819816194576394,  # tsukumo sana
    1409784760805650436,  # ceres fauna
    1409817096523968513,  # ouro kronii
    1409817941705515015,  # nanashi mumei
    1409783149211443200  # hakos baelz
]

EN_TEMPUS_TWITTER_ID = [
    1536575088996524032,  # regis altare
    1536576325296996352,  # magni dezmond
    1536577295632441344,  # axel syrios
    1536579341332516864  # noir vesper
]

EN_TWITTER_ID = EN_MYTH_TWITTER_ID + EN_VSINGER_TWITTER_ID + EN_COUNCIL_TWITTER_ID + EN_TEMPUS_TWITTER_ID
