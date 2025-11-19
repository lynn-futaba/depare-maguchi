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
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000051'); 8156
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000052'); 8157
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000053'); 8158
UPDATE `eip_signal`.`word_output` SET `value` = '1' WHERE (`tag` = 'a_Depallet_w_w') and (`address` = '00000054'); 8159