



const APP_ID = sessionStorage.getItem('appid')
const TOKEN = sessionStorage.getItem('token')
const CHANNEL = sessionStorage.getItem('room')

const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}
//let curruser=sessionStorage.getItem('user')

console.log("stream connected ")
let UID=Number(sessionStorage.getItem('UID'));
let appid=sessionStorage.getItem('appid')
//let username=sessionStorage.getItem('username')
let userstr=sessionStorage.getItem('userstr')
userstr=userstr.split(" ")
let uidstr=sessionStorage.getItem('uidstr')
uidstr=uidstr.split(" ")
console.log(userstr)
console.log(uidstr)
let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL

    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)
    //UID = await client.join(APP_ID, CHANNEL, TOKEN, null)
    try{
        await client.join(appid, CHANNEL, TOKEN, UID)
    }catch(error){
        console.error(error)
        //window.open('/', '_self')
    }
    
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    let username=""
    for (let i=0; i<userstr.length-1;i++)
    {
        if (UID==uidstr[i])
        {
            username=userstr[i]
        }
    }
    //let member = await createMember()

    let player = `<div  class="video-container" id="user-container-${UID}">
                     <div class="video-player" id="user-${UID}"></div>
                     <div class="username-wrapper"><span class="user-name">${username}</span></div>
                  </div>`
    
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
    localTracks[1].play(`user-${UID}`)
    await client.publish([localTracks[0], localTracks[1]])
}



console.log("working")
let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)
    //console.log("this one"+curruser)
    if (mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null){
            player.remove()
        }
        let username=""
        for (let i=0; i<userstr.length-1;i++)
        {
            if (user.uid==uidstr[i])
            {
                username=userstr[i]
            }
        }
        //let member = await getMember(user)

        player = `<div  class="video-container" id="user-container-${user.uid}">
            <div class="video-player" id="user-${user.uid}"></div>
            <div class="username-wrapper"><span class="user-name">${username}</span></div>
        </div>`

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }

    if (mediaType === 'audio'){
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}



let leaveAndRemoveLocalStream = async () => {
    for (let i=0; localTracks.length > i; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }

    await client.leave()
    //This is somewhat of an issue because if user leaves without actaull pressing leave button, it will not trigger
    //deleteMember()
    window.open('/', '_self')
}

let toggleCamera = async (e) => {
    console.log('TOGGLE CAMERA TRIGGERED')
    if(localTracks[1].muted){
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }else{
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

let toggleMic = async (e) => {
    console.log('TOGGLE MIC TRIGGERED')
    if(localTracks[0].muted){
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }else{
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}




joinAndDisplayLocalStream()


document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)