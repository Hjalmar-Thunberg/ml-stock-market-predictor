import type { NextPage } from "next";
import React from "react";
import AreaGraph from "components/Graph";
import api from "../api";

const Home: NextPage = () => {
	return (
		<div>
			<button onClick={() => {
				api.get('get-pred/TSLA').then(response => {
					console.log(response.data)
				})
			}}>Get Prediction Test</button>
			<button onClick={() => {
				api.get('admin/train/AAPL').then(response => {
					console.log(response.data)
				})
			}}>Admin Train Model</button>
			<button onClick={() => {
				api.get('admin/models/RBLX').then(response => {
					console.log(response.data)
				})
			}}>Admin Get Model</button>
			<AreaGraph width={1600} height={600} />
		</div>
	);
};

export default Home;
