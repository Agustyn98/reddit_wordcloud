CREATE VIEW reddit_dataset.view_total_argentina AS (
SELECT word, SUM(count) as count FROM `reddit_dataset.words`
WHERE subreddit = "argentina"
AND LENGTH(word) > 1
AND word NOT IN (select * from reddit_dataset.stop_words)
AND word NOT IN ('savevideo', 'of', 'the', 'is', 'that', 'for', 'to', 'haria', 'viene', 'salio', 've', 'ademas', 'in', 'veo', 'salir', 'quiero', 'gusta', 'alla', 'amp', 'pasar', 'pasa', 're', 'x200b', 'decis', 'pone', 'vi', 'sale', 'deberia')
GROUP BY word
);


CREATE VIEW reddit_dataset.view_words_without_stopwords AS (
SELECT * FROM `reddit_dataset.words`
WHERE
LENGTH(word) > 1
AND word NOT IN (select * from reddit_dataset.stop_words)
AND word NOT IN ('savevideo', 'of', 'the', 'is', 'that', 'for', 'to', 'haria', 'viene', 'salio', 've', 'ademas', 'in', 'veo', 'salir', 'quiero', 'gusta', 'alla', 'amp', 'pasar', 'pasa', 're', 'x200b', 'decis', 'pone', 'vi', 'sale', 'deberia')
);
