cat example.json |python jparser.py
cat example.json |python jparser.py --format "{@timestamp} 1 {@fields[status_code]}"
cat example.json |python jparser.py --filter @fields.level=INFO
cat example.json |python jparser.py --filter @fields.level__ne=INFO
cat example.json |python jparser.py --filter @fields.level__in=IN --filter @fields.level__in=FO
e.t.c.
