

        // [{"model": "api.categoryicon", "pk": 1, "fields": {"ci_class": "13324234"}}]
let    linecons=['linecons-music', 'linecons-search', 'linecons-mail', 'linecons-heart', 'linecons-star', 'linecons-user', 'linecons-videocam', 'linecons-camera', 'linecons-photo', 'linecons-attach', 'linecons-lock', 'linecons-eye', 'linecons-tag', 'linecons-thumbs-up', 'linecons-pencil', 'linecons-comment', 'linecons-location', 'linecons-cup', 'linecons-trash', 'linecons-doc', 'linecons-note', 'linecons-cog', 'linecons-params', 'linecons-calendar', 'linecons-sound', 'linecons-clock', 'linecons-lightbulb', 'linecons-tv', 'linecons-desktop', 'linecons-mobile', 'linecons-cd', 'linecons-inbox', 'linecons-globe', 'linecons-cloud', 'linecons-paper-plane', 'linecons-fire', 'linecons-graduation-cap', 'linecons-megaphone', 'linecons-database', 'linecons-key', 'linecons-beaker', 'linecons-truck', 'linecons-money', 'linecons-food', 'linecons-shop', 'linecons-diamond', 'linecons-t-shirt', 'linecons-wallet']
// let    linecons=['banknote.png', 'bubble.png', 'bulb.png', 'calendar.png', 'camera.png', 'clip.png', 'clock.png', 'cloud.png', 'cup.png', 'data.png', 'diamond.png', 'display.png', 'eye.png', 'fire.png', 'food.png', 'heart.png', 'key.png', 'lab.png', 'like.png', 'location.png', 'lock.png', 'mail.png', 'megaphone.png', 'music.png', 'news.png', 'note.png', 'paperplane.png', 'params.png', 'pen.png', 'phone.png', 'photo.png', 'search.png', 'settings.png', 'shop.png', 'sound.png', 'stack.png', 'star.png', 'study.png', 't-shirt.png', 'tag.png', 'trash.png', 'truck.png', 'tv.png', 'user.png', 'vallet.png', 'video.png', 'vynil.png', 'world.png']
res=[]
for(var i=0,len=linecons.length;i<len;i++){
    res.push({"model": "api.categoryicon", "pk": i+1, "fields": {"ci_class": linecons[i].split('.')[0]}})
}

console.log(JSON.stringify(res))