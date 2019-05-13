
export function getAllBp(){
    return fetch("http://localhost:9000/requestsForApi",{
        method:'GET'
    })
    .then(res => {
        return(res.json())
    });
};

export function getAllBpCarStatus(){
    return fetch("http://localhost:9000/RoadStatus",{
        method:'GET'
    })
    .then(res =>{
        return(res.json())
    })
}
export function getAllBpFactoryStatus() {
    return fetch("http://localhost:9000/FactoryStatus", {
        method: 'GET'
    })
        .then(res => {
            return (res.json())
        })
}
export function createNewBp(object){
    fetch("http://localhost:9000/BallPlacesApi",{
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