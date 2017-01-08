CREATE
OR REPLACE FUNCTION VN_FUNC_Report_Store (
	empl_id INTEGER,
	date_from CHARACTER VARYING,
	date_to CHARACTER VARYING,
	store_id INTEGER
) RETURNS TABLE (
	company_name CHARACTER VARYING,
	employee_name CHARACTER VARYING,
	sale_order_number BIGINT,
	total_sale_amount NUMERIC,
	return_order_number BIGINT,
	total_return_amount NUMERIC,
	total_sale NUMERIC,
	company_name1 CHARACTER VARYING,
	sum_sale_order NUMERIC,
	sum_total_sale_amount NUMERIC,
	sum_return_order_number NUMERIC,
	sum_total_return_amount NUMERIC,
	sum_total_sale NUMERIC
) AS $BODY$
BEGIN
	RETURN QUERY SELECT
		*
	FROM
		(
			(
				SELECT
					*
				FROM
					VN_FUNC_Get_Store_From_Date_To_Date (
						empl_id,
						date_from,
						date_to,
						store_id
					)
			) AS tmp1
			JOIN (
				SELECT
					*
				FROM
					VN_FUNC_Get_Total_Store_From_Date_To_Date (
						empl_id,
						date_from,
						date_to,
						store_id
					)
			) AS tmp2 ON tmp1.company_name = tmp2.company_name
		) ;
	END $BODY$ LANGUAGE plpgsql;