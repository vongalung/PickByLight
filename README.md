# PickByLight
**PT. Apparel One Indonesia's warehouse management Pick-By-Light Project**

## PYTHON DEPENDECIES
- `psycopg2-binary >= 2.7.5`
- `pyModbusTCP >= 0.1.8`

## SYSTEM REQUIREMENTS
- `Python >= 3.6`
- `PostgreSQL >= 9.5`

## HARDWARE (FOR LIGHT CONTROLS)
- Autonics ARM Series modbus sensor connector type digital remote I/O
- Menics MWE Series LED signal lights

## DESCRIPTION
This is a specific project used in **PT. Apparel One Indonesia** as factory warehouse management tools, specifically on warehouse racking management. It uses **Autonics ARM Series modbus connector type digital remote I/O (ARM)** to drive the **Menics MWE Series LED signal lights (MWE Lights)** as the racking lights.

## SETTING UP SYSTEM (SERVER SIDE)
- Create a table in PostgreSQL
  `CREATE TABLE rpi_request (
    req_id NUMERIC,
    locators TEXT,
    user_id NUMERIC,
    req_time TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    CONSTRAINT rpi_request_pkey PRIMARY KEY (req_id)
  );`
  This table shall serve as the project's temporary lights-up-requests container.
- Set up your PostgreSQL configuration in `config/database.py`
  `DB_HOST` : Specifies your server's address (DEFAULT : **'localhost'**)
  `DB_NAME` : Put the name of the previously created temporary table here (DEFAULT : **'rpi_request'**)
  `DB_PORT` : The server's PostgreSQL port (DEFAULT : **'5432'**)
- You may also want to adjust your specific ARM configurations in `config/modbus.py` (e.g : the modbus devices addresses, the ARM pin mapping corresponding to the MWE Lights colors, etc.)

## HOW IT WORKS
The program will lights-up the specific **MWE Lights** corresponding to the specific slots in the racks, based on a given request. These given requests shall be sent/inserted into a specific table in the **PostgreSQL** database (explained on the [SETTING UP SYSTEM (SERVER SIDE)](https://github.com/vongalung/PickByLight#setting-up-system-server-side) section above).
The function `modules.psql.psql_get.psql_get()` will then retrieve these requests. The program will then utilizes `threading` to handle each of these lights-up requests, which in turn will pass the requests to `modules.modbus.rack_modbus.execute()` to lights-up the **MWE Lights** one by one. The `modules.modbus.rack_modbus` script utilizes `pyModbusTCP.client.ModbusClient().write_multiple_registers()` so that it may handle multiple **MWE Lights** lights-up request in one go.

## CHANGELOG
- Created at 2018-11-15 10:05
