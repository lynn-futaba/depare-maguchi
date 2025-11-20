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

But did not insert any data to parts_supply database   
INSERT INTO depal.parts_supply (inventory_id,case_quantity) VALUES (%s,%s);"
