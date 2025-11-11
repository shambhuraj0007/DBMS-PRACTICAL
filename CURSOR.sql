SET SERVEROUTPUT ON;

DROP TABLE o_rollcall1 CASCADE CONSTRAINTS;
DROP TABLE n_rollcall1 CASCADE CONSTRAINTS;

CREATE TABLE o_rollcall1(
    rno INT,
    name VARCHAR2(20),
    status VARCHAR2(30)
);

CREATE TABLE n_rollcall1(
    rno INT,
    name VARCHAR2(20),
    status VARCHAR2(30)
);

INSERT INTO o_rollcall1 VALUES(1, 'Anisha', 'Present');
INSERT INTO o_rollcall1 VALUES(2, 'Summit', 'Present');
INSERT INTO o_rollcall1 VALUES(3, 'Ram', 'Present');
INSERT INTO o_rollcall1 VALUES(4, 'Ramesh', 'Absent');
INSERT INTO o_rollcall1 VALUES(5, 'Harshal', 'Present');

INSERT INTO n_rollcall1 VALUES(2, 'Summit', 'Present');
INSERT INTO n_rollcall1 VALUES(3, 'Ram', 'Present');
INSERT INTO n_rollcall1 VALUES(6, 'Isha', 'Present');

SELECT * FROM o_rollcall1;

SELECT * FROM n_rollcall1;

--tables created and data inserted

COMMIT;

BEGIN
    UPDATE o_rollcall1 SET status = 'Absent' WHERE rno = 5;
    IF SQL%FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Updated');
    END IF;
    IF SQL%ROWCOUNT > 0 THEN
        DBMS_OUTPUT.PUT_LINE(SQL%ROWCOUNT || ' row(s) updated');
    ELSE
        DBMS_OUTPUT.PUT_LINE('No rows updated');
    END IF;
END;
/

DECLARE
    CURSOR explicit_cur IS
        SELECT rno, name, status FROM o_rollcall1 WHERE status = 'Present';
    tmp explicit_cur%ROWTYPE;
    v_count NUMBER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- EXPLICIT CURSOR ---');
    OPEN explicit_cur;
    LOOP
        FETCH explicit_cur INTO tmp;
        EXIT WHEN explicit_cur%NOTFOUND;
        v_count := v_count + 1;
        DBMS_OUTPUT.PUT_LINE('ROLLNO: ' || tmp.rno ||
                             '   NAME: ' || tmp.name ||
                             '   STATUS: ' || tmp.status);
    END LOOP;
    DBMS_OUTPUT.PUT_LINE(v_count || ' row(s) found');
    CLOSE explicit_cur;
END;
/

DECLARE
    CURSOR for_cur IS
        SELECT rno, name, status FROM o_rollcall1 WHERE status = 'Absent';
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- FOR LOOP CURSOR ---');
    FOR tmp IN for_cur LOOP
        DBMS_OUTPUT.PUT_LINE('ROLLNO: ' || tmp.rno ||
                             '   NAME: ' || tmp.name ||
                             '   STATUS: ' || tmp.status);
    END LOOP;
END;
/

DECLARE
    v_roll_no NUMBER;
    CURSOR param_cur(p_roll NUMBER) IS
        SELECT * FROM o_rollcall1 WHERE rno = p_roll;
BEGIN
    v_roll_no := &roll;
    FOR tmp IN param_cur(v_roll_no) LOOP
        DBMS_OUTPUT.PUT_LINE('Roll No: ' || tmp.rno);
        DBMS_OUTPUT.PUT_LINE('Name: ' || tmp.name);
        DBMS_OUTPUT.PUT_LINE('Status: ' || tmp.status);
    END LOOP;
END;
/
----now input roll number

BEGIN
    MERGE INTO n_rollcall1 t1
    USING (SELECT rno, name, status FROM o_rollcall1) t2
    ON (t1.rno = t2.rno)
    WHEN MATCHED THEN
        UPDATE SET t1.name = t2.name,
                   t1.status = t2.status
    WHEN NOT MATCHED THEN
        INSERT (rno, name, status)
        VALUES (t2.rno, t2.name, t2.status);
    DBMS_OUTPUT.PUT_LINE('Merged ' || SQL%ROWCOUNT || ' row(s)');
END;
/

SELECT * FROM o_rollcall1 ORDER BY rno;
SELECT * FROM n_rollcall1 ORDER BY rno;

--An explicit cursor is a cursor that you create manually in PL/SQL when a query returns multiple rows.
You must:

--DECLARE the cursor-OPEN it-FETCH from it- and then close it.


--✅ Why do we use explicit cursors?

--To process each row one-by-one from a SELECT query that returns multiple rows.

--What is an Implicit Cursor?

--An implicit cursor is automatically created by Oracle when you execute a SQL statement like
--You do not declare it.
--Oracle manages opening, fetching, and closing internally.

--A parameterized explicit cursor is a cursor that accepts parameters, just like a function.
--This allows the cursor to run the same SQL query with different values each time.