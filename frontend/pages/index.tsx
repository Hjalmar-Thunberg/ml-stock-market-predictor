import type { NextPage } from "next";
import React from "react";
import AreaGraph from "components/Graph";

const Home: NextPage = () => {
	return (
		<div>
			<AreaGraph width={1600} height={600} />
		</div>
	);
};

export default Home;
