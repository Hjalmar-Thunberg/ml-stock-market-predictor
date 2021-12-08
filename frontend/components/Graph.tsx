import React, { useMemo, useCallback, useState, useEffect } from "react";
import { AreaClosed, Line, Bar } from "@visx/shape";
import { curveMonotoneX } from "@visx/curve";
import { GridRows, GridColumns } from "@visx/grid";
import { scaleTime, scaleLinear } from "@visx/scale";
import {
	withTooltip,
	Tooltip,
	TooltipWithBounds,
	defaultStyles,
} from "@visx/tooltip";
import { WithTooltipProvidedProps } from "@visx/tooltip/lib/enhancers/withTooltip";
import { localPoint } from "@visx/event";
import { LinearGradient } from "@visx/gradient";
import { max, extent, bisector } from "d3-array";
import { timeFormat } from "d3-time-format";
import { AutoComplete } from "components";
import api from "../api";

type GraphStock = {
	date: string;
	close: number;
};

type TooltipData = GraphStock;

export const background = "#3b6978";
export const background2 = "#204051";
export const accentColor = "#edffea";
export const accentColorDark = "#75daad";
const tooltipStyles = {
	...defaultStyles,
	background,
	border: "1px solid white",
	color: "white",
};

// util
const formatDate = timeFormat("%b %d, '%y");

// accessors
const getDate = (d: GraphStock) => new Date(d.date);
const getStockValue = (d: GraphStock) => d.close;
const bisectDate = bisector<GraphStock, Date>((d) => new Date(d.date)).left;

const getInitialData = async (): Promise<GraphStock[]> => {
	let data: GraphStock[] = [];
	await api.get("get-pred/AAPL/").then((response) => {
		const res = response.data.Close;
		for (const i in res) {
			const v: GraphStock = {
				date: response.data.Date[i].split(" ")[0],
				close: Math.round(res[i] * 100) / 100,
			};
			data.push(v);
		}
	});
	data = data.splice(data.length - 60);
	return data || [{ date: "2021-11-22", close: 161.0200042725 }];
};

export type AreaProps = {
	width: number;
	height: number;
	margin?: { top: number; right: number; bottom: number; left: number };
};

export default withTooltip<AreaProps, TooltipData>(
	({
		width,
		height,
		margin = { top: 0, right: 0, bottom: 0, left: 0 },
		showTooltip,
		hideTooltip,
		tooltipData,
		tooltipTop = 0,
		tooltipLeft = 0,
	}: AreaProps & WithTooltipProvidedProps<TooltipData>) => {
		if (width < 10) return null;

		const [stockData, setStockData] = useState<GraphStock[]>([
			{ date: "2021-11-22", close: 161.0200042725 },
		]);

		useEffect(() => {
			getInitialData()
				.then((data) => {
					console.log(data);
					setStockData(data);
				})
				.catch((err) => console.log(err));
		}, []);

		// bounds
		const innerWidth = width - margin.left - margin.right;
		const innerHeight = height - margin.top - margin.bottom;

		// scales
		const dateScale = useMemo(
			() =>
				scaleTime({
					range: [margin.left, innerWidth + margin.left],
					domain: extent(stockData, getDate) as [Date, Date],
				}),
			[innerWidth, margin.left],
		);
		const stockValueScale = useMemo(
			() =>
				scaleLinear({
					range: [innerHeight + margin.top, margin.top],
					domain: [0, (max(stockData, getStockValue) || 0) + innerHeight / 3],
					nice: true,
				}),
			[margin.top, innerHeight],
		);

		// tooltip handler
		const handleTooltip = useCallback(
			(
				event:
					| React.TouchEvent<SVGRectElement>
					| React.MouseEvent<SVGRectElement>,
			) => {
				const { x } = localPoint(event) || { x: 0 };
				const x0 = dateScale.invert(x);
				const index = bisectDate(stockData, x0, 1);
				const d0 = stockData[index - 1];
				const d1 = stockData[index];
				let d = d0;
				if (d1 && getDate(d1)) {
					d =
						x0.valueOf() - getDate(d0).valueOf() >
						getDate(d1).valueOf() - x0.valueOf()
							? d1
							: d0;
				}
				showTooltip({
					tooltipData: d,
					tooltipLeft: x,
					tooltipTop: stockValueScale(getStockValue(d)),
				});
			},
			[showTooltip, stockValueScale, dateScale],
		);

		return (
			<div>
				<AutoComplete setData={setStockData} />
				{stockData.length > 1 && (
					<svg width={width} height={height}>
						<rect
							x={0}
							y={0}
							width={width}
							height={height}
							fill="url(#area-background-gradient)"
							rx={14}
						/>
						<LinearGradient
							id="area-background-gradient"
							from={background}
							to={background2}
						/>
						<LinearGradient
							id="area-gradient"
							from={accentColor}
							to={accentColor}
							toOpacity={0.1}
						/>
						<GridRows
							left={margin.left}
							scale={stockValueScale}
							width={innerWidth}
							strokeDasharray="1,3"
							stroke={accentColor}
							strokeOpacity={0}
							pointerEvents="none"
						/>
						<GridColumns
							top={margin.top}
							scale={dateScale}
							height={innerHeight}
							strokeDasharray="1,3"
							stroke={accentColor}
							strokeOpacity={0.2}
							pointerEvents="none"
						/>
						<AreaClosed<GraphStock>
							data={stockData}
							x={(d) => dateScale(getDate(d)) ?? 0}
							y={(d) => stockValueScale(getStockValue(d)) ?? 0}
							yScale={stockValueScale}
							strokeWidth={1}
							stroke="url(#area-gradient)"
							fill="url(#area-gradient)"
							curve={curveMonotoneX}
						/>
						<Bar
							x={margin.left}
							y={margin.top}
							width={innerWidth}
							height={innerHeight}
							fill="transparent"
							rx={14}
							onTouchStart={handleTooltip}
							onTouchMove={handleTooltip}
							onMouseMove={handleTooltip}
							onMouseLeave={() => hideTooltip()}
						/>
						{tooltipData && (
							<g>
								<Line
									from={{ x: tooltipLeft, y: margin.top }}
									to={{ x: tooltipLeft, y: innerHeight + margin.top }}
									stroke={accentColorDark}
									strokeWidth={2}
									pointerEvents="none"
									strokeDasharray="5,2"
								/>
								<circle
									cx={tooltipLeft}
									cy={tooltipTop + 1}
									r={4}
									fill="black"
									fillOpacity={0.1}
									stroke="black"
									strokeOpacity={0.1}
									strokeWidth={2}
									pointerEvents="none"
								/>
								<circle
									cx={tooltipLeft}
									cy={tooltipTop}
									r={4}
									fill={accentColorDark}
									stroke="white"
									strokeWidth={2}
									pointerEvents="none"
								/>
							</g>
						)}
					</svg>
				)}
				{tooltipData && (
					<div>
						<TooltipWithBounds
							key={Math.random()}
							top={tooltipTop - 12}
							left={tooltipLeft + 12}
							style={tooltipStyles}>
							{`$${getStockValue(tooltipData)}`}
						</TooltipWithBounds>
						<Tooltip
							top={innerHeight + margin.top - 14}
							left={tooltipLeft}
							style={{
								...defaultStyles,
								minWidth: 72,
								textAlign: "center",
								transform: "translateX(-50%)",
							}}>
							{formatDate(getDate(tooltipData))}
						</Tooltip>
					</div>
				)}
			</div>
		);
	},
);
