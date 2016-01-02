module Main where

import           Control.Monad
import           Data.Function
import           Data.List
import           System.Environment

import           CV.ConnectedComponents
import qualified CV.Drawing             as D
import           CV.Fitting
import           CV.HighGUI
import           CV.Image
import           CV.ImageMath
import           CV.ImageOp
import           CV.Thresholding
import           CV.Video

main :: IO ()
main = do
  args <- getArgs
  if length args > 1
    then do
      cap <- captureFromFile (args !! 2)
      detectWith cap
    else do
      Just cap <- captureFromCam 0
      detectWith cap

getBackground :: Capture -> IO [Image RGB D32]
getBackground cap = do
  win <- makeWindow "Background"
  imgs <- replicateM 10 $ do
    waitKey 50
    Just image <- getFrame cap
    showImage "Background" (image <# D.putTextOp (0,255,0) 1.5 "Cogiendo capturas del fondo" (50, 50))
    return image
  destroyWindow "Background"
  return imgs


detectWith :: Capture -> IO ()
detectWith cap = do
  (x:_) <- getBackground cap
  win <- makeWindow "Take sample"
  loop x
  waitKey 0
  destroyWindow "Take sample"
  where
    -- loop :: IO ()
    loop x = do
      Just image <- getFrame cap -- here
      showImage "Take sample" image
      --showImage "Take sample" (absDiff (rgbToGray x) (rgbToGray image))
      --getHand $ unsafeImageTo8Bit (absDiff (rgbToGray x) (rgbToGray image))
      key <- waitKey 10
      unless (key /= -1) (loop x)

getHand :: Image GrayScale D8 -> IO ()
getHand img = do
  let img' = threshold ZeroAndMax 5 img
  -- let img' = adaptiveThreshold ByGaussian MaxAndZero 5 0.2 img
  let contours = getContours ContourAll img'
  let maxContour = maximumBy (compare `on` contourArea) contours
  --showImage "Take sample" $ drawContour 0 255 Immediate (LineOf 5) (0,0) img' maxContour
  showImage "Take sample" img'
  return ()
