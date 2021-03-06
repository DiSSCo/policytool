import {unref} from 'vue'

export const PACK_STATUS = {
    COMPLETE: 'complete',
    INCOMPLETE: 'incomplete',
    NOT_STARTED: 'not_started',
}

export const calcPackStatus = (pack) => {
    pack = unref(pack)
    if (!!pack.finished_at) {
        return PACK_STATUS.COMPLETE
    } else if (pack['answered'] === 0) {
        return PACK_STATUS.NOT_STARTED
    } else {
        return PACK_STATUS.INCOMPLETE
    }
}

export const clamp = (num, min, max) => Math.min(Math.max(num, min), max);
