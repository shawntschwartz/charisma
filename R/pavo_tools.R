# Mirror matrices about x axis
#  https://github.com/rmaia/pavo/blob/master/R/plot.rimg.R
mirrorx <- function(x) {
  if (length(dim(x)) == 3) {
    for (i in seq_len(dim(x)[3])) {
      x[, , i] <- x[, , i][, rev(seq_len(ncol(x[, , i])))]
    }
  } else {
    x <- x[, rev(seq_len(ncol(x)))]
  }
  return(x)
}

rgb_euc_dist <- function(rgb_table_altered, c1, c2) {
  euc_dist <- sqrt((rgb_table_altered[c1, "col1"]
                    - rgb_table_altered[c2, "col1"])^2
                   + (rgb_table_altered[c1, "col2"]
                      - rgb_table_altered[c2, "col2"])^2) %>%
    .[1,1]
  return(euc_dist)
}

rgb_lum_dist <- function(rgb_table_altered, c1, c2) {
  lum_dist <- sqrt((rgb_table_altered[c1, "lum"]
                    - rgb_table_altered[c2, "lum"])^2) %>%
    .[1,1]
  return(lum_dist)
}

# input is a single classified image
calcEucLumDists <- function(classified_image) {
  # extract RGB values for n colors
  class_rgb <- attr(classified_image, 'classRGB')
  class_rgb_altered <- class_rgb %>%
    rownames_to_column(var = "col_num") %>%
    as_tibble %>%
    mutate(col1 = (R - G) / (R + G),
           col2 = (G - B) / (G + B),
           lum = R + G + B) %>%
    select(col1, col2, lum)

  # create matrix to hold colors based on the num of possible color comparisons
  euc_dists <- matrix(nrow = choose(nrow(class_rgb), 2), ncol = 4)

  combos_simple <- t(combn(rownames(class_rgb), 2)) %>%
    as_tibble(.name_repair = 'unique') %>%
    transmute(c1 = as.numeric(`...1`), c2 = as.numeric(`...2`)) %>%
    as.data.frame()

  combos <- matrix(nrow = nrow(combos_simple), ncol = 4)

  for (i in 1:nrow(combos_simple)) {
    combos[i, 1] <- combos_simple[i, 1]
    combos[i, 2] <- combos_simple[i, 2]
    combos[i, 3] <- rgb_euc_dist(class_rgb_altered,combos_simple[i, 1],
                                 combos_simple[i, 2])
    combos[i, 4] <- rgb_lum_dist(class_rgb_altered,combos_simple[i, 1],
                                 combos_simple[i, 2])
  }

  combos <- combos %>%
    as.data.frame %>%
    as_tibble %>%
    dplyr::rename(c1 = V1,
                  c2 = V2,
                  dS = V3,
                  dL = V4) %>%
    as.data.frame

  return(combos)
}

# get distance data frame for each picture
get_img_class_k_dists <- function(classifications, euclidean_lum_dists) {
  return(purrr::map(.x = classifications, .f = euclidean_lum_dists))
}

# calculate the adjacency stats for each image,
#  using the calculated distances as proxies for dS and dL
get_adj_stats <- function(classifications, img_class_k_dists, imagedata2,
                          xpts = 100, xscale = 100, bkgID = NULL) {
  adj_k_dists_list <- list()
  for (i in 1:length(classifications)) {
    adj_k_dists_list[[i]] <- pavo::adjacent(classimg = classifications[[i]],
                                            coldists = img_class_k_dists[[i]],
                                            xpts = xpts, xscale = xscale,
                                            bkgID = as.numeric(bkgID))
    cat("\n")
  }

  return(adj_k_dists_list)
}

# clean up and select relevant stats
get_cleaned_up_stats <- function(adj_k_dists_list) {
  img_adj_k_dists <- Reduce(plyr::rbind.fill, adj_k_dists_list) %>%
    rownames_to_column(var = "name") %>%
    as_tibble()

  img_adj_k_dists_select <- img_adj_k_dists %>%
    dplyr::select(name, m, m_r, m_c, A, Sc, St, Jc, Jt, m_dS, s_dS,
                  cv_dS, m_dL, s_dL, cv_dL)

  return(img_adj_k_dists_select)
}

pavo_classify_charisma <- function(charisma_obj, k_override = NULL, plot = T) {
  # create tmp filepath
  tmp_out_target <- file.path(tempdir(), basename(charisma_obj$path))

  # get number of colors classes to classify in pavo
  if (is.null(k_override)) {
    charisma_k_cols <- charisma_obj$k
  } else {
    charisma_k_cols <- k_override
  }


  # save out tmp recolored jpeg
  #  inherit out_type from current file extension
  #  also determine if mask should be rendered with threshold
  #   depending on whether there were any dropped colors
  use_threshold <- FALSE

  if (length(charisma_obj$dropped_colors) > 0) {
    use_threshold <- TRUE
  }

  charisma_to_img(charisma_obj, out_type = tools::file_ext(charisma_obj$path),
                  render_method = 'array', render_with_threshold = use_threshold,
                  filename = tmp_out_target)

  # read back in
  pavo_img <- suppressMessages(pavo::getimg(tmp_out_target, max.size = 3))

  # run classification
  #  remember, this includes the background color as one of the k classes which
  #   can be identified to be excluded before running the adjacency analyses
  pavo_class <- pavo::classify(pavo_img, kcols = charisma_k_cols + 1)
  classifications <- list()
  classifications[[1]] <- pavo_class

  # manually transform image
  ## adapted from: https://github.com/rmaia/pavo/blob/master/R/plot.rimg.R
  img3 <- rev(t(apply(pavo_class, 1, rev))) # mirror
  dim(img3) <- dim(pavo_class)
  img <- t(apply(img3, 2, rev)) # rotate 90
  rgbs <- attr(pavo_class, "classRGB") # reconstitute image

  mapR <- setNames(rgbs$R, seq_len(nrow(rgbs)))
  mapG <- setNames(rgbs$G, seq_len(nrow(rgbs)))
  mapB <- setNames(rgbs$B, seq_len(nrow(rgbs)))
  R <- matrix(mapR[img], nrow = nrow(img), dimnames = dimnames(img))
  G <- matrix(mapG[img], nrow = nrow(img), dimnames = dimnames(img))
  B <- matrix(mapB[img], nrow = nrow(img), dimnames = dimnames(img))

  imageout <- array(c(R, G, B), dim = c(dim(img)[1], dim(img)[2], 3))

  # convert and transform
  imagedata2 <- suppressWarnings(as.raster(imageout))
  imagedata2 <- mirrorx(imagedata2)
  imagedata2 <- apply(t(as.matrix(imagedata2)), 2, rev)

  if (plot) {
    plot_pavo_input(charisma_obj, imagedata2, mar = c(5.1, 4.1, 4.1, 2.1))
  }

  tmp_pavo_cols <- attr(pavo_class, "classRGB")

  ## TODO: this works for now as an ID to pass into the pavo adjaceny function,
  ##  but will fail if there are multiple ID's that fall within the white
  ##  boundary, so it'll be critical to figure out an elegant solution for this!
  white_bg_id <- rownames(subset(tmp_pavo_cols,
                                 rowSums(tmp_pavo_cols[,1:3] > 0.99) > 0))

  tmp_pavo_cols <- subset(tmp_pavo_cols,
                          rowSums(tmp_pavo_cols[,1:3] > 0.99) == 0)

  palette <- rgb(tmp_pavo_cols)

  if (plot) {
    plot_pavo_pal(charisma_obj, k = charisma_k_cols, pal = palette,
                  mar = c(5.1, 4.1, 4.1, 2.1))
  }

  # get relevant coldists data before running adjacency
  classified_k_dists <- suppressMessages(
    get_img_class_k_dists(classifications, calcEucLumDists)
  )
  adj_stats_raw <- get_adj_stats(classifications = classifications,
                                 img_class_k_dists = classified_k_dists,
                                 imagedata2 = imagedata2, bkgID = white_bg_id)
  adj_stats <- get_cleaned_up_stats(adj_stats_raw)

  output.list <- vector("list", length = 4)
  output.list_names <- c("input2pavo",
                         "adj_stats",
                         "adj_class",
                         "adj_class_plot_cols")
  names(output.list) <- output.list_names

  output.list$input2pavo <- imagedata2
  output.list$adj_stats <- adj_stats
  output.list$adj_class <- tmp_pavo_cols
  output.list$adj_class_plot_cols <- palette

  return(output.list)
}
