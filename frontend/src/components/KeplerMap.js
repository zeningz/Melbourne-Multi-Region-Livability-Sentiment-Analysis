import React, {useEffect} from 'react';
import keplerGlReducer from 'kepler.gl/reducers';
import {createStore, combineReducers, applyMiddleware} from 'redux';
import {taskMiddleware} from 'react-palm/tasks';
import { Provider, useDispatch } from 'react-redux';
import KeplerGl from "kepler.gl";
import { addDataToMap } from "kepler.gl/actions";
import useSwr from "swr";

const reducers = combineReducers({
    keplerGl: keplerGlReducer
});
  
const store = createStore(reducers, {}, applyMiddleware(taskMiddleware));

export default function keplerMap (props){
    console.log(props.data)
    var combine  = []

    var dateHash = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    };

    var featureJson = [
        {"name": "Summary Type","format":"","type":"string"},
        {"name": "Date","format":"YYYY-M-D H:m:s","type":"timestamp"},
        {"name": "latitude","format":"","type":"real"},
        {"name": "longitude","format":"","type":"real"},
        {"name": "area","format":"","type":"string"},
        {"name": "value","format":"","type":"integer"}
    ]
    for (var key of Object.keys(props.data)){
        var curRow = []
        if (key !== "status"){
            for (var kkey of  Object.keys(props.data[key])){
                for (var i =0;i<props.data[key][kkey].length;i++){
                    var date = props.data[key][kkey][i]["date"].split("-")
                    var replaceDate = date[0]+"-"+dateHash[date[1]]+"-"+date[2]+" 00:00:00 +10:00"
                    curRow.push([key,replaceDate,props.data[key][kkey][i]["coord"][1],props.data[key][kkey][i]["coord"][0],props.data[key][kkey][i]["area"],props.data[key][kkey][i]["value"]])
                }
                    
            }
        }
        combine.push({ "fields":featureJson,"rows":curRow})
    }
    return(
        <Provider store={store}>
            <Map data = {combine} />
        </Provider>
    )
}



function Map(props) {
    const dispatch = useDispatch();
    const {data} = useSwr("covid", async () =>{
        const datas = props.data; //await response.json();
        return datas;
    });
    useEffect(() => {
        if (data) {
            dispatch(
                addDataToMap({
                    datasets: [{
                        info: {
                            label: data[0]["rows"][0][0],
                            id: data[0]["rows"][0][0]
                        },
                        data:data[0]
                    },
                    {
                        info: {
                            label: data[1]["rows"][0][0],
                            id: data[1]["rows"][0][0]
                        },
                        data:data[1]
                    },
                    {
                        info: {
                            label: data[2]["rows"][0][0],
                            id: data[2]["rows"][0][0]
                        },
                        data:data[2]
                    },
                    {
                        info: {
                            label: data[3]["rows"][0][0],
                            id: data[3]["rows"][0][0]
                        },
                        data:data[3]
                    },
                    {
                        info: {
                            label: data[4]["rows"][0][0],
                            id: data[4]["rows"][0][0]
                        },
                        data:data[4]
                    },
                    {
                        info: {
                            label: data[5]["rows"][0][0],
                            id: data[5]["rows"][0][0]
                        },
                        data:data[5]
                    },
                ],
                    
                    option: {
                        centerMap: true,
                        readOnly: false
                    },
                    config: {}
                })
            );
        }
    }, [dispatch, data]);

    return(
        <div>
            <KeplerGl
                id="covid"
                mapboxApiAccessToken= {process.env.REACT_APP_MAPBOX_API}
                width={window.innerWidth}
                height={window.innerHeight}
            />
        </div>
    )
}