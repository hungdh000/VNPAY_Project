CREATE
OR REPLACE FUNCTION VN_FUNC_Get_Sale_Order_Date (
	empl_id INTEGER,
	date_from CHARACTER VARYING,
	date_to CHARACTER VARYING,
	store_id INTEGER
) RETURNS TABLE (
	company_name CHARACTER VARYING,
	employee_name CHARACTER VARYING,
	order_date DATE,
	sale_order_number BIGINT,
	total_sale_amount NUMERIC,
	return_order_number BIGINT,
	total_return_amount NUMERIC,
	total_sale NUMERIC
) AS $BODY$
BEGIN

IF store_id = - 1
AND empl_id = - 1 THEN
	RETURN QUERY SELECT
		order_tmp1.company_name,
		order_tmp1.employee_name,
		order_tmp1.date_order,
		order_tmp1.sale_order_number,
		order_tmp1.total_sale_amount,
		order_tmp2.return_order_number,
		order_tmp2.total_return_amount,
		CASE
	WHEN order_tmp2.total_return_amount < 0 THEN
		order_tmp1.total_sale_amount + order_tmp2.total_return_amount
	ELSE
		order_tmp1.total_sale_amount
	END AS total_sale
	FROM
		(
			SELECT
				pos_order.date_order :: DATE,
				"user"."name" AS employee_name,
				comp. NAME AS company_name,
				COUNT (pos_order."name") AS sale_order_number,
				SUM (pos_order.amount_total) AS total_sale_amount
			FROM
				pos_order AS pos_order
			INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
			AND pos_order.user_id = "user"."id"
			AND pos_order.write_uid = "user"."id"
			INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
			WHERE
				pos_order.date_order :: DATE BETWEEN date_from :: DATE
			AND date_to :: DATE
			AND pos_order."state" IN ('paid', 'invoice', 'done')
			AND pos_order.amount_total >= 0
			GROUP BY
				pos_order.date_order :: DATE,
				comp. NAME,
				"user"."name"
			ORDER BY
				pos_order.date_order :: DATE
		) AS order_tmp1
	LEFT JOIN (
		SELECT
			pos_order.date_order :: DATE,
			"user"."name" AS employee_name,
			comp. NAME AS company_name,
			COUNT (pos_order."name") AS return_order_number,
			SUM (pos_order.amount_total) AS total_return_amount
		FROM
			pos_order AS pos_order
		INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
		AND pos_order.user_id = "user"."id"
		AND pos_order.write_uid = "user"."id"
		INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
		WHERE
			pos_order.date_order :: DATE BETWEEN date_from :: DATE
		AND date_to :: DATE
		AND pos_order."state" IN ('paid', 'invoice', 'done')
		AND pos_order.amount_total < 0
		GROUP BY
			pos_order.date_order :: DATE,
			comp. NAME,
			"user"."name"
		ORDER BY
			pos_order.date_order :: DATE
	) AS order_tmp2 ON order_tmp1.employee_name = order_tmp2.employee_name
	AND order_tmp1.company_name = order_tmp2.company_name
	AND order_tmp1.date_order = order_tmp2.date_order ;
	ELSIF store_id != - 1
	AND empl_id = - 1 THEN
		RETURN QUERY SELECT
			order_tmp1.company_name,
			order_tmp1.employee_name,
			order_tmp1.date_order,
			order_tmp1.sale_order_number,
			order_tmp1.total_sale_amount,
			order_tmp2.return_order_number,
			order_tmp2.total_return_amount,
			CASE
		WHEN order_tmp2.total_return_amount < 0 THEN
			order_tmp1.total_sale_amount + order_tmp2.total_return_amount
		ELSE
			order_tmp1.total_sale_amount
		END AS total_sale
		FROM
			(
				SELECT
					pos_order.date_order :: DATE,
					"user"."name" AS employee_name,
					comp. NAME AS company_name,
					COUNT (pos_order."name") AS sale_order_number,
					SUM (pos_order.amount_total) AS total_sale_amount
				FROM
					pos_order AS pos_order
				INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
				AND pos_order.user_id = "user"."id"
				AND pos_order.write_uid = "user"."id"
				INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
				WHERE
					pos_order.date_order :: DATE BETWEEN date_from :: DATE
				AND date_to :: DATE
				AND pos_order."state" IN ('paid', 'invoice', 'done')
				AND pos_order.amount_total >= 0
				AND pos_order.company_id = store_id
				GROUP BY
					pos_order.date_order :: DATE,
					comp. NAME,
					"user"."name"
				ORDER BY
					pos_order.date_order :: DATE
			) AS order_tmp1
		LEFT JOIN (
			SELECT
				pos_order.date_order :: DATE,
				"user"."name" AS employee_name,
				comp. NAME AS company_name,
				COUNT (pos_order."name") AS return_order_number,
				SUM (pos_order.amount_total) AS total_return_amount
			FROM
				pos_order AS pos_order
			INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
			AND pos_order.user_id = "user"."id"
			AND pos_order.write_uid = "user"."id"
			INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
			WHERE
				pos_order.date_order :: DATE BETWEEN date_from :: DATE
			AND date_to :: DATE
			AND pos_order."state" IN ('paid', 'invoice', 'done')
			AND pos_order.amount_total < 0
			AND pos_order.company_id = store_id
			GROUP BY
				pos_order.date_order :: DATE,
				comp. NAME,
				"user"."name"
			ORDER BY
				pos_order.date_order :: DATE
		) AS order_tmp2 ON order_tmp1.employee_name = order_tmp2.employee_name
		AND order_tmp1.company_name = order_tmp2.company_name
		AND order_tmp1.date_order = order_tmp2.date_order ;
		ELSIF store_id != - 1
		AND empl_id != - 1 THEN
			RETURN QUERY SELECT
				order_tmp1.company_name,
				order_tmp1.employee_name,
				order_tmp1.date_order,
				order_tmp1.sale_order_number,
				order_tmp1.total_sale_amount,
				order_tmp2.return_order_number,
				order_tmp2.total_return_amount,
				CASE
			WHEN order_tmp2.total_return_amount < 0 THEN
				order_tmp1.total_sale_amount + order_tmp2.total_return_amount
			ELSE
				order_tmp1.total_sale_amount
			END AS total_sale
			FROM
				(
					SELECT
						pos_order.date_order :: DATE,
						"user"."name" AS employee_name,
						comp. NAME AS company_name,
						COUNT (pos_order."name") AS sale_order_number,
						SUM (pos_order.amount_total) AS total_sale_amount
					FROM
						pos_order AS pos_order
					INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
					AND pos_order.user_id = "user"."id"
					AND pos_order.write_uid = "user"."id"
					INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
					WHERE
						pos_order.date_order :: DATE BETWEEN date_from :: DATE
					AND date_to :: DATE
					AND pos_order."state" IN ('paid', 'invoice', 'done')
					AND pos_order.amount_total >= 0
					AND pos_order.company_id = store_id
					AND pos_order.user_id = empl_id
					GROUP BY
						pos_order.date_order :: DATE,
						comp. NAME,
						"user"."name"
					ORDER BY
						pos_order.date_order :: DATE
				) AS order_tmp1
			LEFT JOIN (
				SELECT
					pos_order.date_order :: DATE,
					"user"."name" AS employee_name,
					comp. NAME AS company_name,
					COUNT (pos_order."name") AS return_order_number,
					SUM (pos_order.amount_total) AS total_return_amount
				FROM
					pos_order AS pos_order
				INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
				AND pos_order.user_id = "user"."id"
				AND pos_order.write_uid = "user"."id"
				INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
				WHERE
					pos_order.date_order :: DATE BETWEEN date_from :: DATE
				AND date_to :: DATE
				AND pos_order."state" IN ('paid', 'invoice', 'done')
				AND pos_order.amount_total < 0
				AND pos_order.company_id = store_id
				AND pos_order.user_id = empl_id
				GROUP BY
					pos_order.date_order :: DATE,
					comp. NAME,
					"user"."name"
				ORDER BY
					pos_order.date_order :: DATE
			) AS order_tmp2 ON order_tmp1.employee_name = order_tmp2.employee_name
			AND order_tmp1.company_name = order_tmp2.company_name
			AND order_tmp1.date_order = order_tmp2.date_order ;
			ELSIF store_id = - 1
			AND empl_id != - 1 THEN
				RETURN QUERY SELECT
					order_tmp1.company_name,
					order_tmp1.employee_name,
					order_tmp1.date_order,
					order_tmp1.sale_order_number,
					order_tmp1.total_sale_amount,
					order_tmp2.return_order_number,
					order_tmp2.total_return_amount,
					CASE
				WHEN order_tmp2.total_return_amount < 0 THEN
					order_tmp1.total_sale_amount + order_tmp2.total_return_amount
				ELSE
					order_tmp1.total_sale_amount
				END AS total_sale
				FROM
					(
						SELECT
							pos_order.date_order :: DATE,
							"user"."name" AS employee_name,
							comp. NAME AS company_name,
							COUNT (pos_order."name") AS sale_order_number,
							SUM (pos_order.amount_total) AS total_sale_amount
						FROM
							pos_order AS pos_order
						INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
						AND pos_order.user_id = "user"."id"
						AND pos_order.write_uid = "user"."id"
						INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
						WHERE
							pos_order.date_order :: DATE BETWEEN date_from :: DATE
						AND date_to :: DATE
						AND pos_order."state" IN ('paid', 'invoice', 'done')
						AND pos_order.amount_total >= 0
						AND pos_order.user_id = empl_id
						GROUP BY
							pos_order.date_order :: DATE,
							comp. NAME,
							"user"."name"
						ORDER BY
							pos_order.date_order :: DATE
					) AS order_tmp1
				LEFT JOIN (
					SELECT
						pos_order.date_order :: DATE,
						"user"."name" AS employee_name,
						comp. NAME AS company_name,
						COUNT (pos_order."name") AS return_order_number,
						SUM (pos_order.amount_total) AS total_return_amount
					FROM
						pos_order AS pos_order
					INNER JOIN "public".res_users AS "user" ON pos_order.create_uid = "user"."id"
					AND pos_order.user_id = "user"."id"
					AND pos_order.write_uid = "user"."id"
					INNER JOIN "public".res_company AS comp ON pos_order.company_id = comp."id"
					WHERE
						pos_order.date_order :: DATE BETWEEN date_from :: DATE
					AND date_to :: DATE
					AND pos_order."state" IN ('paid', 'invoice', 'done')
					AND pos_order.amount_total < 0
					AND pos_order.user_id = empl_id
					GROUP BY
						pos_order.date_order :: DATE,
						comp. NAME,
						"user"."name"
					ORDER BY
						pos_order.date_order :: DATE
				) AS order_tmp2 ON order_tmp1.employee_name = order_tmp2.employee_name
				AND order_tmp1.company_name = order_tmp2.company_name
				AND order_tmp1.date_order = order_tmp2.date_order ;
				END
				IF ;
				END $BODY$ LANGUAGE plpgsql;