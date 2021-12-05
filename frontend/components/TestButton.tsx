import React, { Component, MouseEvent } from "react";
import axios from "axios";

type Props = {
	message: string;
};
type State = {
	count: number;
};

export default class TestButton extends Component<Props, State> {
	constructor(props: Props) {
		super(props);
		this.state = {
			count: 0,
		};

		this.sendTestRequest = this.sendTestRequest.bind(this);
	}

	sendTestRequest(event: MouseEvent) {
		event.preventDefault();
		axios({
			url: "http://localhost:8000/test/",
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

	render() {
		return <button onClick={this.sendTestRequest}>Click me pl0x</button>;
	}
}
