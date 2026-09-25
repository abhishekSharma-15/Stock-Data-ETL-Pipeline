# INSERT_STOCK_INFO = """
#     INSERT INTO stock_info (
#         symbol,
#         company_name,
#         exchange
#     )
#     VALUES (
#         :symbol,
#         :company_name,
#         :exchange
#     )
#     ON CONFLICT (symbol) DO UPDATE
#         SET company_name = EXCLUDED.company_name
#     RETURNING stock_id;
# """

INSERT_STOCK_INFO = """
    WITH inserted AS (
        INSERT INTO stock_info (symbol, company_name, exchange)
        VALUES (:symbol, :company_name, :exchange)
        ON CONFLICT (symbol) DO NOTHING
        RETURNING stock_id
    )
    SELECT stock_id FROM inserted
    UNION ALL
    SELECT stock_id FROM stock_info WHERE symbol = :symbol
    LIMIT 1;
"""

GET_STOCK_ID = """
    SELECT stock_id
    FROM stock_info
    WHERE symbol = :symbol;
"""
