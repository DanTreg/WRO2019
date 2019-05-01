
export function getAllBp(){
    return fetch("http://localhost:9000/requestsForApi",{
        method:'GET'
    })
    .then(res => {
        return(res.json())
    });
};


export function createNewBp(object){
    fetch("http://localhost:9000/read_json",{
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