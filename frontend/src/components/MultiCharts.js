import React from "react";
import PieDiagram from "./PieDiagram";
import BarDiagram from "./BarDiagram";
import {Panel,Grid,} from "rsuite"
import {Row,Col} from "antd";
import "antd/dist/antd.css";
import "rsuite/dist/rsuite.min.css";
import MultiBar from "./MutliBar";
import MultiBarA from "./MutliBarA";


export default function MultiCharts(props){
    console.log(props.data)
    var housing = []
    var educateSentiSum = []
    var educatePloarSum = []
    var educateSentiCount = []
    var educatePloarCount = []
    var houseSentiSum = []
    var housePloarSum = []
    var houseSentiCount = []
    var housePloarCount = []
    var educatePloarCombine = []
    var educateSentiCombine = []
    var housePloarCombine = []
    var houseSentiCombine = []
    var outPairs = []
    var pairs  = [["Syd","Rest_of_NSW"],["Ade","Rest_of_SA"],["MEL","Rest_of_VIC"],["BRI","Rest_of_QLD"]]
    
    if (props.type === "aurin"){
        for (const key in props.data){
            if (!key.includes("level") && key !== "status"){
                let curVal = {
                    key : key,
                    data : props.data[key]
                }
                housing.push(curVal)
            }
        }
        for(var i =0;i<pairs.length;i++){
            var cur=[]
            for (var j=0;j<pairs[i].length;j++){
                let curVal = {
                    key : pairs[i][j],
                    data : props.data[pairs[i][j]]
                }
                cur.push(curVal) 
            }
            outPairs.push(cur)
        }
    }

    function combineBardata(key,calc,output,types,inves){
        var yearSum = {
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2022": 0,
        }
        for (var kkey in props.data[key]){
            var curOut = {"key": calc + " of " + types+ " about "+inves + " in "+kkey  }
            var cur = []
            if (key.includes(calc) && key.includes(types)){
                for (var i =0;i<props.data[key][kkey].length;i++){
                    var date = props.data[key][kkey][i]["date"].split("-")
                    if(date[0] in yearSum){
                        yearSum[date[0]]+=props.data[key][kkey][i]["value"]
                    }
                }
                for (var years of Object.keys(yearSum)){
                    if (yearSum[years] !== 0 ){
                        let curVal = {
                            key : years,
                            data : yearSum[years]
                        }
                        cur.push(curVal)
                    }
                }
                curOut["data"] = cur
                output.push(curOut)
            }
        }
    }
    
    for (var key in props.data){
        if (key !== "status"){
            if (key.includes("educt")){
                combineBardata(key,"sum",educateSentiSum,"sentiment","education")
                combineBardata(key,"sum",educatePloarSum,"polarity","education")
                combineBardata(key,"count",educateSentiCount,"sentiment","education")
                combineBardata(key,"count",educatePloarCount,"polarity","education")
            }
            if (key.includes("hous")){
                combineBardata(key,"sum",houseSentiSum,"sentiment","housing")
                combineBardata(key,"sum",housePloarSum,"polarity","housing")
                combineBardata(key,"count",houseSentiCount,"sentiment","housing")
                combineBardata(key,"count",housePloarCount,"polarity","housing")
            }
        }
    }
    function combineBarVal(output,direc,types,flag){
        var yearSum = {
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2022": 0,
        }
        var yearCount = {
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2022": 0,
        }
        for (var key in props.data){
            
            if (key.includes(direc)&&key.includes(types)){
                console.log(key)
                var isFound = false
                for (var kkey in props.data[key]){
                    var curOut = {"key": "combine of " + direc+ " about "+types + " in "+kkey  }
                    var cur = []
                    if(key.includes("count")){
                        for (var i =0;i<props.data[key][kkey].length;i++){
                            var date = props.data[key][kkey][i]["date"].split("-")
                            if(date[0] in yearCount){
                                yearCount[date[0]]+=props.data[key][kkey][i]["value"]
                            }
                        }
                        if (flag ===1){
                            isFound = true
                        }
                    }
                    if(key.includes("sum")){
                        for (var j =0;j<props.data[key][kkey].length;j++){
                            var dates = props.data[key][kkey][j]["date"].split("-")
                            if(dates[0] in yearSum){
                                yearSum[dates[0]]+=props.data[key][kkey][j]["value"]
                            }
                        }
                        if (flag ===0){
                            isFound=true
                        }
                    }
                    for (var years of Object.keys(yearSum)){
                        if (yearSum[years] !== 0 && yearCount[years] !== 0){
                            let curVal = {
                                key : years,
                                data : yearSum[years]/yearCount[years]
                            }
                            cur.push(curVal)
                        }
                    }
                    if (isFound){
                        curOut["data"] = cur
                        output.push(curOut)
                    }
                }
            }
        }
    }

    combineBarVal(educatePloarCombine,"polarity","eduction",0)
    combineBarVal(educateSentiCombine,"sentiment","eduction",0)
    combineBarVal(housePloarCombine,"polarity","housing",1)
    combineBarVal(houseSentiCombine,"sentiment","housing",0)
    const aurinOutput =() =>{
        return(
            <div>
                <Grid fluid width={window.innerWidth} height={window.innerHeight}>
                    <Row className="show-grid" gutter={[16, 16]}>
                        
                        <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>Bar Diagram for Housing price Among Australia {"(unit: million $AUD)"}</p>
                                <div style={{ margin: "55px", textAlign: "center" }}>
                                <MultiBarA data={housing}/>
                                </div>
                            </Panel>
                        </Col>

                        {outPairs.map((items,index)=>{
                            return (
                            <Col span={12} key = {index}>
                                <Panel shaded bordered expanded>
                                    <p>Bar Diagram for Housing price Among {items[0][Object.keys(items[0])[0]]} and {items[1][Object.keys(items[1])[0]]} {"(unit: million $AUD)"}</p>
                                    <div style={{ margin: "55px", textAlign: "center" }}>
                                        <MultiBarA data={items}/>
                                    </div>
                                </Panel>
                            </Col>
                            )
                        })}
                        {Object.keys(props.data).map((datas, index)=>{
                                return (
                                    datas==="status" ? null :
                                        datas.includes("level") ? 
                                        <Col span={12} key={index}> 
                                            <Panel shaded bordered expanded>
                                                <p>Pie Diagram for Education level in {datas}</p>
                                                <div style={{ margin: "55px", textAlign: "center" }}>
                                                    <PieDiagram data={props.data[datas]}/>
                                                </div>
                                            </Panel>
                                        </Col>
                                        : null
                                        
                                )
                        })}
                        
                    </Row>
                </Grid>
            </div>
        )
    }

    const tweetOutput= () =>{
        return (
            <div>
                <Grid fluid width={window.innerWidth} height={window.innerHeight}>
                    <Row className="show-grid" gutter={[16, 16]}>
                        { housePloarCount.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{housePloarCount[0]["key"]}</p>
                                    <BarDiagram data={housePloarCount[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>count of polarity about housing in Melbourn</p>
                                <MultiBar data={housePloarCount}/>
                            </Panel>
                        </Col>}

                        { housePloarSum.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{housePloarSum[0]["key"]}</p>
                                    <BarDiagram data={housePloarSum[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>sum of polarity about housing in Melbourn</p>
                                <MultiBar data={housePloarSum}/>
                            </Panel>
                        </Col>}
                    </Row>
                    <Row className="show-grid" gutter={[16, 16]}>
                        { houseSentiCount.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{houseSentiCount[0]["key"]}</p>
                                    <BarDiagram data={houseSentiCount[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>count of sentiment about housing in Melbourn</p>
                                <MultiBar data={houseSentiCount}/>
                            </Panel>
                        </Col>}

                        { houseSentiSum.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{houseSentiSum[0]["key"]}</p>
                                    <BarDiagram data={houseSentiSum[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>sum of sentiment about housing in Melbourn</p>
                                <MultiBar data={houseSentiSum}/>
                            </Panel>
                        </Col>}
                    </Row>
                    <Row className="show-grid" gutter={[16, 16]}>
                        { housePloarCombine.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{housePloarCombine[0]["key"]}</p>
                                    <BarDiagram data={housePloarCombine[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>combine of polarity about housing in Melbourn</p>
                                <MultiBar data={housePloarCombine}/>
                            </Panel>
                        </Col>}

                        { houseSentiCombine.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{houseSentiCombine[0]["key"]}</p>
                                    <BarDiagram data={houseSentiCombine[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>combine of sentiment about housing in Melbourn</p>
                                <MultiBar data={houseSentiCombine}/>
                            </Panel>
                        </Col>}

                    </Row>
                    <Row className="show-grid" gutter={[16, 16]}>
                        { educatePloarCount.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{educatePloarCount[0]["key"]}</p>
                                    <BarDiagram data={educatePloarCount[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>count of polarity about education in Melbourn</p>
                                <MultiBar data={educatePloarCount}/>
                            </Panel>
                        </Col>}

                        { educatePloarSum.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{educatePloarSum[0]["key"]}</p>
                                    <BarDiagram data={educatePloarSum[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>sum of polarity about education in Melbourn</p>
                                <MultiBar data={educatePloarSum}/>
                            </Panel>
                        </Col>}
                    </Row>
                    <Row className="show-grid" gutter={[16, 16]}>
                        { educateSentiCount.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{educateSentiCount[0]["key"]}</p>
                                    <BarDiagram data={educateSentiCount[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>count of sentiment about education in Melbourn</p>
                                <MultiBar data={educateSentiCount}/>
                            </Panel>
                        </Col>}

                        { educateSentiSum.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{educateSentiSum[0]["key"]}</p>
                                    <BarDiagram data={educateSentiSum[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>sum of sentiment about education in Melbourn</p>
                                <MultiBar data={educateSentiSum}/>
                            </Panel>
                        </Col>}
                    </Row>
                    <Row className="show-grid" gutter={[16, 16]}>
                        { educatePloarCombine.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{educatePloarCombine[0]["key"]}</p>
                                    <BarDiagram data={educatePloarCombine[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>combine of polarity about education in Melbourn</p>
                                <MultiBar data={educatePloarCombine}/>
                            </Panel>
                        </Col>}

                        { educateSentiCombine.length === 1 ?
                                <Col span={12}>
                                <Panel shaded bordered expanded>
                                    <p>{educateSentiCombine[0]["key"]}</p>
                                    <BarDiagram data={educateSentiCombine[0]["data"]}/>
                                </Panel>
                            </Col>
                        : <Col span={12}>
                            <Panel shaded bordered expanded>
                                <p>combine of sentiment about education in Melbourn</p>
                                <MultiBar data={educateSentiCombine}/>
                            </Panel>
                        </Col>}

                    </Row>
                </Grid>
            </div>
        )
    }
    return (
        <div>
            {props.type==="aurin"? aurinOutput(): null}
            {props.type==="tweet"? tweetOutput(): null}
        </div>
    )
}