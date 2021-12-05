import React, { useState } from "react";
import Select from "react-select";
import axios from "axios";

function grabDataForSelected(selectedOption: { value: unknown }) {
	axios({
		url: `http://localhost:8000/get-model-data/${selectedOption.value}`,
		method: "GET",
		headers: {
			"Access-Control-Allow-Origin": "*",
		},
		proxy: {
			host: "127.0.0.1",
			port: 8080,
		},
	})
		.then((response) => {
			console.log(response.data.Close);
			const res = [];
			for (const i in response.data.Close) {
				res.push(i);
			}
			console.log(res.slice(res.length - 100, res.length));
		})
		.catch((err) => {
			console.log(err);
		});
}

export const AutoComplete = () => {
	const [selectedOption, setSelectedOption] = useState<any>(null);

	return (
		<div className="App">
			<Select
				defaultValue={selectedOption}
				onChange={(selectedOption) => {
					setSelectedOption(selectedOption);
					grabDataForSelected(selectedOption);
				}}
				options={options}
			/>
		</div>
	);
};

const options = [
	{ label: "AAPL", value: "AAPL" },
	{ label: "MSFT", value: "MSFT" },
	{ label: "GOOGL", value: "GOOGL" },
	{ label: "GOOG", value: "GOOG" },
	{ label: "AMZN", value: "AMZN" },
	{ label: "TSLA", value: "TSLA" },
	{ label: "FB", value: "FB" },
	{ label: "NVDA", value: "NVDA" },
	{ label: "TSM", value: "TSM" },
	{ label: "JPM", value: "JPM" },
	{ label: "UNH", value: "UNH" },
	{ label: "HD", value: "HD" },
	{ label: "JNJ", value: "JNJ" },
	{ label: "V", value: "V" },
	{ label: "WMT", value: "WMT" },
	{ label: "BAC", value: "BAC" },
	{ label: "BABA", value: "BABA" },
	{ label: "PG", value: "PG" },
	{ label: "ADBE", value: "ADBE" },
	{ label: "ASML", value: "ASML" },
	{ label: "MA", value: "MA" },
	{ label: "PFE", value: "PFE" },
	{ label: "NFLX", value: "NFLX" },
	{ label: "CRM", value: "CRM" },
	{ label: "NKE", value: "NKE" },
	{ label: "DIS", value: "DIS" },
];
