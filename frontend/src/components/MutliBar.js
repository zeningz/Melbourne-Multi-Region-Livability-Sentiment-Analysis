import React from "react";
import {BarChart,BarSeries} from "reaviz"

export default function MultiBar(props){

        return (
              <BarChart
                width={700}
                height={400}
                data={props.data}
                margins={22.25}
                series={
                  <BarSeries
                    type="grouped"
                    padding={0.7}
                  />
                }
              />
        );
}