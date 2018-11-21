# PickByLight
**[PT. Apparel One Indonesia](http://aoi.co.id/v2/)'s warehouse management Pick-By-Light Project**

## PYTHON DEPENDENCIES
- `psycopg2-binary >= 2.7.5`
- `pyModbusTCP >= 0.1.8`

## SYSTEM REQUIREMENTS
- `Python >= 3.6`
- `PostgreSQL >= 9.5`

## HARDWARE (FOR LIGHT CONTROLS)
- [Autonics ARM Series modbus connector type digital remote I/O (ARM)](http://autonics.se/produkt/arm-series/)
- [Menics MWE Series LED signal lights (MWE Lights)](http://www.autonics.se/produkt/mwe-series/)

## DESCRIPTION
This is a specific project used in [**PT. Apparel One Indonesia**](http://aoi.co.id/v2/) as factory warehouse management tools, specifically on warehouse racking management. It uses **ARM** to drive the **MWE Lights** as the racking lights.

## SETTING UP SYSTEM (SERVER SIDE)
1. Create a table in **PostgreSQL**. This table shall serve as the project's temporary lights-up-requests container.
    ```
    CREATE TABLE rack_automations (
        id character(36) NOT NULL,
        locator_name text,
        group_id integer NOT NULL DEFAULT 0,
        created_at timestamp(0) without time zone,
        updated_at timestamp(0) without time zone,
        po_buyer character varying(255),
        CONSTRAINT rack_automations_pkey PRIMARY KEY (id)
    );
    ```
  
2. Set up your PostgreSQL configuration in `config/database.py` as follows:
      - `DB_HOST` : Specifies your server's address (DEFAULT : **'localhost'**)
      - `DB_PORT` : The server's **PostgreSQL** port (DEFAULT : **'5432'**)
  
3. You may also want to adjust your specific ARM configurations in `config/modbus.py` (e.g : the modbus devices addresses, the ARM pin mapping corresponding to the MWE Lights colors, etc.)

## HOW IT WORKS
The program will lights-up the specific **MWE Lights** corresponding to the specific slots in the racks, based on a given request. These given requests shall be sent/inserted into table `rpi_request` in the **PostgreSQL** database.

The function `modules.psql.psql_get.psql_get()` will then retrieve these requests. The program will then utilizes `threading` to handle each of these lights-up requests, which in turn will pass the requests to `modules.modbus.rack_modbus.execute()` to lights-up the **MWE Lights** one by one. The `modules.modbus.rack_modbus` script utilizes `pyModbusTCP.client.ModbusClient().write_multiple_registers()` so that it may handle multiple **MWE Lights** lights-up request in one go.

## CHANGELOG
- 2018-11-15 - Project created
- 2018-11-21 - Adjusts the script configurations to mirror those applied during the actual project implementation; Minor adjustment to exceptions handling in main.py; and bug fixing
