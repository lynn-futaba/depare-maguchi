"shelf": 
 { "id": "flow_rack", 
  "type": "2", 
  "rack": [{"id": "1", "part": {"id": "1001-0001", "kanban_id": "101", "name": "1001-0001", "car_model_id": "1"}, 
  "case_quantity": "0"}, "None", 
  {"id": "2", "part": {"id": "1001-0002", "kanban_id": "102", "name": "1001-0002", "car_model_id": "2"}, 
  "case_quantity": "0"}, "None"], 
  "dest_line_frontage_id": "0"},


  signal_id testing ->　8156, 8157, 8158, 8159, 8160, 8161, 8162, 8163, 8164

# For is_frontage_ready == true testing
  ready 8100,8101,8102,8103,8104 -> signal_id -> value = 1

SELECT * FROM eip_signal.word_output WHERE signal_id IN (8100,8101,8102,8103,8104)

UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w') and (`address` = '00000000'); signal_id IN (8100,8101,8102,8103,8104)
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w') and (`address` = '00000001');
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w') and (`address` = '00000002');
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w') and (`address` = '00000003');
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w') and (`address` = '00000004');

# For get_kotatsu  
SELECT * FROM `eip_signal`.word_output WHERE signal_id IN (8153, 8155, 8157, 8159, 8161, 8163, 8154, 8156, 8158, 8160, 8162, 8164) 
ORDER BY signal_id;

UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000048'); signal_id 8153
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000049'); signal_id 8154
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000050'); signal_id 8155
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000051'); 8156 -> 0
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000052'); 8157 -> 0
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000053'); 8158
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000054'); 8159


================================================================================
Flowrack API testing
================================================================================
Flowrack GET API
"{\"id\": \"flow_rack\", \"type\": \"2\", 
\"rack\": [
    {\"id\": \"1\", 
    \"part\": {\"id\": \"1001-0001\", \"kanban_id\": \"101\", \"name\": \"1001-0001\", \"car_model_id\": \"1\"}, \"case_quantity\": \"0\"}, \"None\",
    {\"id\": \"2\", 
    \"part\": {\"id\": \"1001-0002\", \"kanban_id\": \"102\", \"name\": \"1001-0002\", \"car_model_id\": \"2\"}, \"case_quantity\": \"0\"}, \"None\"
 ],
 \"dest_line_frontage_id\": \"0\"}"

How to test ==> click complete button from flowrack.html, then updated value for eip_signal.word_input from 0 to 1 in the 129 database.

SELECT signal_id FROM eip_signal.word_input where value = 1;
'4501'
'4514'
'4516'
'4517'
'4519'
'8031'
'8046'
'8060'
'8201'
'8216'
'8231'
'8246'
'8260'
'9030'
'1032'

Error ==> But did not insert any data to parts_supply database   
INSERT INTO depal.parts_supply (inventory_id,case_quantity) VALUES (%s,%s);"

================================================================================
insert_target_ids API + call_target_ids testing
================================================================================
# Bライン, L1 , L2 to check after click (5, 4, 3, 2, 1)
SELECT * from `eip_signal`.word_input WHERE signal_id IN (8504, 8503, 8502, 8501, 8500, 8260, 8246, 8231, 8216, 8201);

# Bライン, L3 to check after click (5, 4, 3)
SELECT * from `eip_signal`.word_input WHERE signal_id IN (8502, 8501, 8500, 8231, 8216, 8200);

# Bライン, R1 to check after click (5, 4, 3, 2, 1)
SELECT * from `eip_signal`.word_input WHERE signal_id IN (8404, 8403, 8402, 8401, 8400, 8061, 8046, 8031, 8016, 8000);

# Bライン, R2 to check after click (5, 4, 3, 2, 1)
SELECT * from `eip_signal`.word_input WHERE signal_id IN (8404, 8403, 8402, 8401, 8400, 8061, 8046, 8032, 8016, 8000);

# Bライン, R3 to check after click (5, 4, 3)
SELECT * from `eip_signal`.word_input WHERE signal_id IN (8404, 8403, 8402, 8060, 8046, 8032);

==================================================================================
Bライン L1

-- 間口に搬送対象idを入力 Bライン L1
SELECT * FROM eip_signal.word_input where signal_id in (8504,8503,8502,8501,8500);
-- 間口に搬送対象を呼び出す Bライン L1
SELECT * FROM eip_signal.word_input where signal_id in (8260,8246,8231,8216,8201);

-- 間口に搬送対象idを入力
-- 呼び出し信号をリセット
SELECT * FROM eip_signal.word_input where signal_id in (8260, 8246, 8231, 8216, 8201);
-- 搬送指示 間口からストアに搬送
SELECT * FROM eip_signal.word_input where signal_id in (8262, 8247, 8232, 8217, 8202);
-- 搬送対象idをリセット
SELECT * FROM eip_signal.word_input where signal_id in (8504, 8503, 8502, 8501, 8500);
-- 搬送指示リセット
SELECT * FROM eip_signal.word_input where signal_id in (8262, 8247, 8232, 8217, 8202);

=================================================================================
call AMR_return
=================================================================================

-- A/B ライン R1,R2 hashiru_ichi 0, hashiru_ni 1, kaeru_ichi 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8061, 8046, 8031, 8016, 8000, 8062, 8047, 8032, 8017, 8002, 8404, 8403, 8402, 8401, 8400 );
-- A/B ライン R1,R2 hashiru_ni 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8062, 8047, 8032, 8017, 8002);

-- A/B ライン R3 hashiru_ichi 0, hashiru_ni 1, kaeru_ichi 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8060, 8046, 8032, 8062, 8047, 8032, 8404, 8403, 8402 );
-- A/B ライン R3 hashiru_ni 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8062, 8047, 8032);
=================================================================================
-- A/B ライン L1/L2 hashiru_ichi 0, hashiru_ni 1, kaeru_ichi 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8260, 8246, 8231, 8216, 8201, 8262, 8247, 8232, 8217, 8202, 8504, 8503, 8502, 8501, 8500 );
-- A/B ライン L1/L2 hashiru_ni 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8262, 8247, 8232, 8217, 8202);


-- A/B ライン L3 hashiru_ichi 0, hashiru_ni 1, kaeru_ichi 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8231, 8216, 8200, 8232, 8217, 8202, 8502, 8501, 8500 );
-- A/B ライン L3 hashiru_ni 0
-- SELECT * FROM eip_signal.word_input where signal_id IN (8232, 8217, 8202);

=================================================================================

-- 間口に搬送対象idを入力 Bライン　L1
-- SELECT * FROM eip_signal.word_input where signal_id in (8504,8503,8502,8501,8500);
-- 間口に搬送対象を呼び出す　1
-- SELECT * FROM eip_signal.word_input where signal_id in (8260,8246,8231,8216,8201);

-- 間口に搬送対象idを入力
-- 呼び出し信号をリセット 0
-- SELECT * FROM eip_signal.word_input where signal_id in (8260, 8246, 8231, 8216, 8201);
-- 搬送指示　間口からストアに搬送 1
-- SELECT * FROM eip_signal.word_input where signal_id in (8262, 8247, 8232, 8217, 8202);
-- 搬送対象idをリセット 0
-- SELECT * FROM eip_signal.word_input where signal_id in (8504, 8503, 8502, 8501, 8500);
-- 搬送指示リセット 0
-- SELECT * FROM eip_signal.word_input where signal_id in (8262, 8247, 8232, 8217, 8202);


-- A/B ライン R1,R2 
SELECT * FROM eip_signal.word_input where signal_id IN (8061, 8046, 8031, 8016, 8000, 8062, 8047, 8032, 8017, 8002, 8404, 8403, 8402, 8401, 8400 )

-- A/B ライン R3
-- SELECT * FROM eip_signal.word_input where signal_id IN (8060, 8046, 8032, 8062, 8047, 8032, 8404, 8403, 8402 );

-- A/B ライン L1,L2 
-- SELECT * FROM eip_signal.word_input where signal_id IN (8260, 8246, 8231, 8216, 8201, 8262, 8247, 8232, 8217, 8202, 8504, 8503, 8502, 8501, 8500 );

-- A/B ライン L3
-- SELECT * FROM eip_signal.word_input where signal_id IN (8231, 8216, 8200, 8232, 8217, 8202, 8502, 8501, 8500 );

-- http://localhost:5000/api/get_depallet_area_by_plat
SELECT mb.plat, ts.step_kanban_no, ts.load_num, ts.shelf_code
            FROM `futaba-chiryu-3building`.t_shelf_status AS ts
            INNER JOIN `futaba-chiryu-3building`.t_location_status AS tl
                ON ts.shelf_code = tl.shelf_code
            INNER JOIN `futaba-chiryu-3building`.m_basis_location AS mb
                ON tl.cell_code = mb.cell_code
            WHERE mb.plat IN (20,21,22,23,24,25,26,27,28,29);

-- t_location_status
SELECT * FROM `futaba-chiryu-3building`.t_location_status where shelf_code IN ('K30147', 'K30148', 'K301497', 'K30150');

SELECT * FROM `futaba-chiryu-3building`.t_location_status where cell_code in (
30550024, 30550023, 30550021, 30550020, 30550018, 30550015, 30550014, 30550012, 30550011, 30550009);

-- m_basis_location
SELECT * FROM `futaba-chiryu-3building`.m_basis_location where plat IN (20,21,22,23,24,25,26,27,28,29);

-- t_shelf_status
SELECT * FROM `futaba-chiryu-3building`.t_shelf_status where shelf_code IN ( 30044,
30066,
30023,
30048);

SELECT * FROM `futaba-chiryu-3building`.t_shelf_status where step_kanban_no in (2004, 2005, 2006, 2001, 2002, 2003);

-- m_plat_status
SELECT * FROM `futaba-chiryu-3building`.m_plat_status where plat in (20,21,22,23,24,25,26,27,28,29);




