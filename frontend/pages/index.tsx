import type { NextPage } from "next";
import React from "react";
import AreaGraph from "components/Graph";
import { AutoComplete } from "components";
import TestButton from "@components/TestButton";

const Home: NextPage = () => {
	return (
		<div>
			<AutoComplete />
			<AreaGraph width={1600} height={600} />
			<TestButton message={"test message"} />
		</div>
	);
};

export default Home;
