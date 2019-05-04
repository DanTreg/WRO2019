
export function getAllBp(){
    return fetch("http://wro2019_api.therdteam.com/requestsForApi",{
        method:'GET'
    })
    .then(res => {
        return(res.json())
    });
};

export function getAllBpCarStatus(){
    return fetch("http://wro2019_api.therdteam.com/RoadStatus",{
        method:'GET'
    })
    .then(res =>{
        return(res.json())
    })
}

export function createNewBp(object){
    fetch("http://wro2019_api.therdteam.com/read_json",{
        method:'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            r:object.Red,
            g:object.Green,
            w:object.White,
            y:object.Yellow,
            b:object.Blue
        })
    })
        .then(res => {return(res)});
};
export default createNewBp;