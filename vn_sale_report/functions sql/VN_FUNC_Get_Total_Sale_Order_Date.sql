CREATE
OR REPLACE FUNCTION VN_FUNC_Get_Total_Sale_Order_Date (
	empl_id INTEGER,
	date_from CHARACTER VARYING,
	date_to CHARACTER VARYING,
	store_id INTEGER
) RETURNS TABLE (
	company_name CHARACTER VARYING,
	order_date DATE,
	sum_sale_order NUMERIC,
	sum_total_sale_amount NUMERIC,
	sum_return_order_number NUMERIC,
	sum_total_return_amount NUMERIC,
	sum_total_sale NUMERIC
) AS $BODY$
BEGIN
	RETURN QUERY SELECT
		order_sale.company_name,
		order_sale.order_date,
		SUM (
			order_sale.sale_order_number
		) AS sum_sale_order,
		SUM (
			order_sale.total_sale_amount
		) AS sum_total_sale_amount,
		SUM (
			order_sale.return_order_number
		) AS sum_return_order_number,
		SUM (
			order_sale.total_return_amount
		) AS sum_total_return_amount,
		SUM (order_sale.total_sale) AS sum_total_sale
	FROM
		(
			SELECT
				*
			FROM
				VN_FUNC_Get_Sale_Order_Date (
					empl_id,
					date_from,
					date_to,
					store_id
				)
		) AS order_sale
	GROUP BY
		order_sale.company_name,
		order_sale.order_date;
	END $BODY$ LANGUAGE plpgsql;