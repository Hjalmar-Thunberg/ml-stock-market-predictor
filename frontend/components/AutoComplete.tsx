import React, { useState } from "react";
import Select from "react-select";
import api from "../api";

type Props = {
	label: string;
	value: string;
};

async function grabDataForSelected({ value }: Props) {
	await api
		.get(`get-model-data/${value}/`)
		.then((response) => {
			const res = response.data.Close;
			const data = [];
			for (const i in res) {
				const v = {
					date: response.data.Date[i].split(" ")[0],
					close: res[i],
				};
				data.push(v);
			}
			return data.slice(data.length - 100, data.length);
		})
		.catch((err) => {
			console.log(err);
		});
}

export const AutoComplete = ({ setData }) => {
	const [selectedOption, setSelectedOption] = useState<any>();

	return (
		<div className="App">
			<Select
				defaultValue={selectedOption}
				onChange={(selectedOption) => {
					setSelectedOption(selectedOption);
					setData(grabDataForSelected(selectedOption));
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
