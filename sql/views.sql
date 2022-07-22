CREATE VIEW [Message Counts] AS
SELECT
  nickname,
  user_id,
  COUNT(*) AS message_count
FROM nicknames JOIN messages
  ON nicknames.user_id = messages.author_id
GROUP BY nickname
ORDER BY COUNT(*) DESC;

CREATE VIEW [Reaction Counts] AS
SELECT
  nickname,
  user_id,
  COUNT(*) AS reaction_count
FROM nicknames JOIN messages
  ON nicknames.user_id = messages.author_id
  JOIN reactions
  ON messages.message_id = reactions.message_id
GROUP BY nickname
ORDER BY COUNT(*) DESC;

CREATE VIEW [Message Dates] AS
SELECT
  DATE(created) as date,
  COUNT(*) as message_count
FROM messages
GROUP BY DATE(created)
ORDER BY created;
  

