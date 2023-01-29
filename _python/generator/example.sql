-- example.sql
-- create tables
% for tablename, tabledata in TABLES.items():
    % if tablename in CREATETABLE_LST:
CREATE TABLE IF NOT EXISTS ${tabledata["SCHEMA"]}.${tablename} (
        % for i, (columnname, column) in enumerate(tabledata["COLUMNS"].items()):
            % if i == 0:
    ${columnname} ${column["DTYPE"]}
            % else:
    ,${columnname} ${column["DTYPE"]}
            % endif
        % endfor
);
    % endif
% endfor

-- grant revoke privileges to schemas
% for tablename, tabledata in TABLES.items():
    % if tablename in GRANT_REVOKE_PRIVILEGES_TABLES_LST:
        % for rolename, privileges in tabledata["ROLEGRANTS"].items():
REVOKE ALL PRIVILEGES ON TABLE ${tabledata["SCHEMA"]}.${tablename} FROM ROLE "${rolename}";
            % for privilege in privileges:
GRANT ${privilege} ON TABLE ${tabledata["SCHEMA"]}.${tablename} TO ROLE "${rolename}";
            % endfor
        % endfor
    % endif
% endfor
